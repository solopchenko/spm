class ServiceAdminForm(ModelForm):
    class Meta:
        model = Service
        widgets = {
            'description': Textarea,
        }
