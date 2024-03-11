from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from habits.models import Habit, Day
from habits.validators import LinkedHabitAndRewardValidator, IsPleasantHabitRewardValidator, IsLinkedToPleasantHabitValidator, \
    IsLinkedToOwnerHabitValidator


class HabitCreateAPISerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    schedule = serializers.PrimaryKeyRelatedField(queryset=Day.objects.all(), many=True, required=False)

    class Meta:
        model = Habit
        fields = '__all__'

        validators = [LinkedHabitAndRewardValidator(),
                      IsPleasantHabitRewardValidator(),
                      IsLinkedToPleasantHabitValidator(),
                      IsLinkedToOwnerHabitValidator(),
                      ]

        def create(self, validated_data):
            schedule_days = validated_data.pop('schedule', None)
            habit = Habit.objects.create(**validated_data)
            if schedule_days:
                habit.schedule.set(schedule_days)
            else:
                all_days = Day.objects.all()
                habit.schedule.set(all_days)
            return habit


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
