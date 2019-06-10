from django import forms
from . import models
from datetime import datetime

from django.core.exceptions import ValidationError

class WorkerForm(forms.ModelForm):

    class Meta:
        model = models.Worker
        fields = [
            'name', 'surname', 'pesel', 'position', 'salary',
            'employment_date', 'promotion_date', 'can_be_subbed_by'
        ]

    def clean_pesel(self):
        data = self.cleaned_data['pesel']

        if int(data) < 10000000000:
            raise ValidationError("Wrong Pesel")

        return data
    
    def clean_salary(self):
        data = self.cleaned_data['salary']

        if int(data) < 0:
            raise ValidationError("Cannot be negative")

        return data

    def clean_can_be_subbed_by(self):
        data = self.cleaned_data['can_be_subbed_by']

        idlist = [d.id for d in data]
        if self.instance.id in idlist:
            raise ValidationError("Cannot sub Yourself")
        return data

    def save(self, commit=True):
        if 'position' in self.changed_data:
            curpos = self.instance.position
            oldpos = models.Position.objects.get(id=self.instance.old_position_id)

            curperms = set(curpos.permissions.all())
            oldperms = set(oldpos.permissions.all())

            gained = list(curperms.difference(oldperms))
            lost = list(oldperms.difference(curperms))

            new_log = models.LogEntry(
                substitute_begin=datetime.now(),
                substitute_end=None,
                subbed=self.instance,
                subbing=None,
                reason=models.PermissionChangeReason.objects.get(desc='awans'),
            )
            new_log.save()
            new_log.old_perms.set(lost)
            new_log.new_perms.set(gained)

        instance = super().save(commit=False)

        if commit:
            instance.save()
            super()._save_m2m()

        return instance


class SubstitutionForm(forms.ModelForm):

    class Meta:
        model = models.Substitution
        fields = [
            'substitute_begin', 'substitute_end', 
            'substituted_worker', 'substituting_worker', 'reason'
        ]

    def clean(self):
        data = super().clean()

        for k,v in data.items():
            if not data[k]:
                raise ValidationError({
                    k: "Wrong"
                })

        if data['substitute_begin'] >= data['substitute_end']:
            raise ValidationError({
                "substitute_begin": "Must be earlier than end",
                "substitute_end": "Must be later than start"
            })

        if data['substituted_worker'] == data['substituting_worker']:
            raise ValidationError({
                "substituted_worker": "Cannot be subbed by itself",
                "substituting_worker": "Cannot be subbing himself"
            })

        if data['substituting_worker'] not in data['substituted_worker'].can_be_subbed_by.all():
            raise ValidationError({
                "substituting_worker": "Cannot be subbing this Worker"
            })

        substituted_set = models.Substitution.objects.filter(substituted_worker=data['substituting_worker'])
        if substituted_set:
            raise ValidationError({
                "substituting_worker": "Someone currently substituted cannot be substituting"
            })

        substituting_set = models.Substitution.objects.filter(substituting_worker=data['substituted_worker'])
        if substituting_set:
            raise ValidationError({
                "substituted_worker": "This Worker is currently substituting someone"
            })

        return data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
            super()._save_m2m()

        subbed = self.instance.substituted_worker
        subbing = self.instance.substituting_worker

        subbedperms = set(subbed.position.permissions.all())
        subbingperms = set(subbing.position.permissions.all())

        gained = subbedperms.difference(subbingperms)

        new_log = models.LogEntry(
            substitute_begin=self.instance.substitute_begin,
            substitute_end=self.instance.substitute_end,
            subbed=subbed,
            subbing=subbing,
            reason=models.PermissionChangeReason.objects.get(desc='zastepstwo'),
        )
        new_log.save()
        new_log.old_perms.set([])
        new_log.new_perms.set(gained)

        return instance

    