from rest_framework import serializers

from habits.models import Habit


class LinkedHabitAndRewardValidator:
    """
    Validator to check if linked_habit and reward fields
    are filled in at the same time.
    """
    def __call__(self, attrs):
        if attrs.get('linked_habit') and attrs.get('reward'):
            raise serializers.ValidationError("Both 'linked_habit' and 'reward' cannot be specified simultaneously.")


class IsPleasantHabitRewardValidator:
    """
    Validator to check the reward in a pleasurable habit.
    There shouldn't be an award.
    """
    def __call__(self, attrs):
        if attrs.get('is_pleasant') and \
                (attrs.get('reward') or attrs.get('linked_habit')):
            raise serializers.ValidationError(
                "If habit is positive, 'linked_habit' and 'reward' should not be specified.")


class IsLinkedToPleasantHabitValidator:
    """
    Validator to check that the link specifies a pleasant habit
    """
    def __call__(self, attrs):
        linked_habit = attrs.get('linked_habit')
        if linked_habit:
            if not linked_habit.is_pleasant:
                raise serializers.ValidationError("'linked_habit' must have 'is_pleasant' set to True.")


class IsLinkedToOwnerHabitValidator:
    """
    Validator to check that the link specifies a pleasant habit
    """
    def __call__(self, attrs):
        linked_habit = attrs.get('linked_habit')
        if linked_habit:
            if not linked_habit.owner == attrs.get('owner'):
                raise serializers.ValidationError("The specified 'linked_habit' does not exist")
