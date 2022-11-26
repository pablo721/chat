from django import forms


class FindUsersForm(forms.Form):
    name = forms.CharField(label='Username', max_length=32,
                           widget=forms.TextInput(attrs={'placeholder': 'Find users/rooms'}))


class CreateRoomForm(forms.Form):
    room_name = forms.CharField(max_length=16, label='Create room', widget=forms.TextInput(attrs={'placeholder': 'Room name..'}))
    private = forms.BooleanField(required=False)


class ClearChatForm(forms.Form):
    all_msgs = forms.BooleanField(label='Delete all messages', initial=False,
                                  help_text='If checked, also deletes incoming messages.')


class InviteToRoom(forms.Form):
    friend = forms.CharField(max_length=32)


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['friend'].choices = [(friend.id, friend.user.username) for friend in request.user.user_profile.friends.all()]


