from rest_framework import serializers

from habits.models import Habit
from habits.validators import LinkedHabitAndRewardValidator, IsPleasantHabitRewardValidator, IsLinkedToPleasantHabitValidator, \
    IsLinkedToOwnerHabitValidator


class HabitCreateAPISerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Habit
        fields = '__all__'

        validators = [LinkedHabitAndRewardValidator(),
                      IsPleasantHabitRewardValidator(),
                      IsLinkedToPleasantHabitValidator(),
                      IsLinkedToOwnerHabitValidator(),
                      ]
