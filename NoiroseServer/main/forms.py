from django import forms
from .models import ComplainBoard

class ComplainBoardForm(forms.ModelForm):
    class Meta:
        model = ComplainBoard
        fields = ['title', 'content']
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
    
        if title and ' ' in title.strip():
            self.add_error('title', '제목에는 공백이 포함될 수 없습니다.')
        
        if content and ' ' in content.strip():
            self.add_error('content', '내용에는 공백이 포함될 수 없습니다.')

