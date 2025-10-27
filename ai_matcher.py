import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

class StudentMatcher:
    """AI-based student matching algorithm for group formation"""

    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def calculate_student_profile(self, student):
        """Create a text profile from student's skills and interests"""
        skills = ' '.join(student.get('skills', []))
        interests = ' '.join(student.get('interests', []))
        bio = student.get('bio', '')
        return f"{skills} {interests} {bio}"

    def calculate_diversity_score(self, group_members):
        """Calculate diversity score based on unique skills in the group"""
        all_skills = set()
        for member in group_members:
            all_skills.update(member.get('skills', []))
        return len(all_skills)

    def suggest_groups(self, students, group_size=5, num_groups=None):
        """
        Suggest optimal groups based on complementary skills and interests

        Args:
            students: List of student dictionaries
            group_size: Target group size (default 5)
            num_groups: Number of groups to form (default: all students / group_size)

        Returns:
            List of suggested groups
        """
        if len(students) < group_size:
            return []

        if num_groups is None:
            num_groups = len(students) // group_size

        # Create profiles for all students
        profiles = [self.calculate_student_profile(s) for s in students]

        # Calculate similarity matrix if students have profiles
        if any(profiles):
            try:
                tfidf_matrix = self.vectorizer.fit_transform(profiles)
                similarity_matrix = cosine_similarity(tfidf_matrix)
            except:
                # If vectorization fails (empty profiles), use random grouping
                similarity_matrix = np.random.rand(len(students), len(students))
        else:
            # Random grouping for students without profiles
            similarity_matrix = np.random.rand(len(students), len(students))

        # Form groups using a greedy approach
        groups = []
        available_students = list(range(len(students)))

        for _ in range(num_groups):
            if len(available_students) < group_size:
                break

            # Start with a random student
            seed_idx = random.choice(available_students)
            group = [seed_idx]
            available_students.remove(seed_idx)

            # Add complementary students (lower similarity = more diverse)
            while len(group) < group_size and available_students:
                # Calculate diversity scores for each potential addition
                best_candidate = None
                best_score = -1

                for candidate_idx in available_students:
                    # Calculate average dissimilarity with current group
                    dissimilarity = np.mean([1 - similarity_matrix[candidate_idx][member]
                                            for member in group])

                    # Prefer diverse students
                    if dissimilarity > best_score:
                        best_score = dissimilarity
                        best_candidate = candidate_idx

                if best_candidate is not None:
                    group.append(best_candidate)
                    available_students.remove(best_candidate)
                else:
                    break

            # Create group with student objects
            group_students = [students[idx] for idx in group]
            groups.append({
                'members': group_students,
                'size': len(group_students),
                'diversity_score': self.calculate_diversity_score(group_students)
            })

        return groups

    def find_best_match_for_student(self, student, available_students, existing_group):
        """
        Find the best student to add to an existing group

        Args:
            student: Student to match
            available_students: List of available students
            existing_group: Current group members

        Returns:
            Best matching student or None
        """
        if not available_students:
            return None

        student_profile = self.calculate_student_profile(student)
        available_profiles = [self.calculate_student_profile(s) for s in available_students]

        # Calculate similarity
        all_profiles = [student_profile] + available_profiles

        try:
            tfidf_matrix = self.vectorizer.fit_transform(all_profiles)
            similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
        except:
            # Random selection if vectorization fails
            return random.choice(available_students)

        # Find most complementary student (lower similarity)
        best_idx = np.argmin(similarities)
        return available_students[best_idx]

    def evaluate_group_compatibility(self, group_members):
        """
        Evaluate how well a group works together

        Returns:
            Score between 0-100
        """
        if len(group_members) < 2:
            return 0

        # Factors:
        # 1. Diversity of skills
        diversity_score = self.calculate_diversity_score(group_members)

        # 2. Common interests
        interest_sets = [set(member.get('interests', [])) for member in group_members]
        common_interests = set.intersection(*interest_sets) if interest_sets else set()

        # 3. Balanced skills
        all_skills = [skill for member in group_members for skill in member.get('skills', [])]
        skill_balance = len(set(all_skills)) / max(len(all_skills), 1)

        # Weighted score
        score = (
            diversity_score * 30 +  # 30% weight on skill diversity
            len(common_interests) * 10 +  # 10 points per common interest
            skill_balance * 50  # 50% weight on skill balance
        )

        return min(100, score)
