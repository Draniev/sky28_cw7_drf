from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

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


class HabitAPIViewSerializer(serializers.ModelSerializer):
    owner = SlugRelatedField(read_only=True, slug_field='username')
    linked_habit = SerializerMethodField(read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'

    def get_linked_habit(self, obj):
        """
        Displays the linked_habit name even in a public Habit
        only if the linked Habit is also public
        """
        request = self.context.get('request')
        linked_habit = obj.linked_habit
        if linked_habit:
            if obj.linked_habit.is_public:
                return linked_habit.name
            else:
                if linked_habit.owner == request.user:
                    return linked_habit.name
                else:
                    return 'secret private habit'
        else:
            return None
