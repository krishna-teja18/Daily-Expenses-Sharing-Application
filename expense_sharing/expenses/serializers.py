from rest_framework import serializers
from .models import Expense, ExpenseParticipant
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile_number']

class ExpenseParticipantSerializer(serializers.ModelSerializer):
    participant_name = serializers.CharField(source='participant.name', read_only=True)  # Get the name of the participant

    class Meta:
        model = ExpenseParticipant
        fields = ['participant', 'participant_name', 'amount', 'percentage']

class ExpenseSerializer(serializers.ModelSerializer):
    participants = ExpenseParticipantSerializer(many=True, required=False)  # Link to participants

    class Meta:
        model = Expense
        fields = ['id', 'creator', 'total_amount', 'split_method', 'participants']

    def create(self, validated_data):
        participants_data = validated_data.pop('participants', [])  # Extract participants data (default to empty list)
        expense = Expense.objects.create(**validated_data)  # Create expense

        for participant_data in participants_data:
            # Create ExpenseParticipant with the participant ID
            ExpenseParticipant.objects.create(expense=expense, **participant_data)
        return expense

    def to_representation(self, instance):
        """Override to_representation to include participants properly."""
        representation = super().to_representation(instance)
        representation['participants'] = ExpenseParticipantSerializer(instance.expense_participants.all(), many=True).data
        return representation
