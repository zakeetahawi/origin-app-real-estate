"""
Core models for Origin App Real Estate Management System.
Includes User Profile, Roles, Permissions, and Audit Log.
"""
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Permission(models.Model):
    """
    Custom permission model for fine-grained access control.
    """
    name = models.CharField(_('Permission Name'), max_length=100, unique=True)
    codename = models.CharField(_('Code Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)
    module = models.CharField(_('Module'), max_length=50, choices=[
        ('core', _('Core')),
        ('owners', _('Owners')),
        ('clients', _('Clients')),
        ('properties', _('Properties')),
        ('contracts', _('Contracts')),
        ('maintenance', _('Maintenance')),
        ('reports', _('Reports')),
        ('api', _('API')),
    ])
    action = models.CharField(_('Action'), max_length=20, choices=[
        ('view', _('View')),
        ('add', _('Add')),
        ('change', _('Change')),
        ('delete', _('Delete')),
        ('export', _('Export')),
        ('import', _('Import')),
        ('manage', _('Manage')),
    ])
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')
        ordering = ['module', 'action']
        unique_together = ['module', 'action']

    def __str__(self):
        return f"{self.module}.{self.action}"


class Role(models.Model):
    """
    Custom role model for role-based access control.
    """
    ROLE_TYPES = [
        ('super_admin', _('Super Admin')),
        ('admin', _('Admin')),
        ('manager', _('Manager')),
        ('user', _('User')),
        ('custom', _('Custom')),
    ]

    name = models.CharField(_('Role Name'), max_length=100, unique=True)
    role_type = models.CharField(_('Role Type'), max_length=20, choices=ROLE_TYPES, default='custom')
    description = models.TextField(_('Description'), blank=True)
    permissions = models.ManyToManyField(Permission, verbose_name=_('Permissions'), blank=True, related_name='roles')
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ['name']

    def __str__(self):
        return self.name

    def has_permission(self, permission_codename):
        """Check if role has a specific permission."""
        return self.permissions.filter(codename=permission_codename).exists()


class UserProfile(models.Model):
    """
    Extended user profile with role and additional information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users', verbose_name=_('Role'))
    phone = models.CharField(_('Phone Number'), max_length=20, blank=True)
    address = models.TextField(_('Address'), blank=True)
    avatar = models.ImageField(_('Avatar'), upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(_('Date of Birth'), null=True, blank=True)
    
    # Preferences
    language = models.CharField(_('Language'), max_length=5, choices=[
        ('en', 'English'),
        ('ar', 'العربية'),
    ], default='en')
    theme = models.CharField(_('Theme'), max_length=10, choices=[
        ('light', _('Light')),
        ('dark', _('Dark')),
    ], default='light')
    
    # Additional info
    employee_id = models.CharField(_('Employee ID'), max_length=50, blank=True)
    department = models.CharField(_('Department'), max_length=100, blank=True)
    position = models.CharField(_('Position'), max_length=100, blank=True)
    
    # Status
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.role}"

    def has_permission(self, permission_codename):
        """Check if user has a specific permission through their role."""
        if self.role:
            return self.role.has_permission(permission_codename)
        return False

    def get_all_permissions(self):
        """Get all permissions for this user through their role."""
        if self.role:
            return self.role.permissions.all()
        return Permission.objects.none()


class AuditLog(models.Model):
    """
    Audit log for tracking all changes in the system.
    """
    ACTION_TYPES = [
        ('create', _('Create')),
        ('update', _('Update')),
        ('delete', _('Delete')),
        ('view', _('View')),
        ('login', _('Login')),
        ('logout', _('Logout')),
        ('export', _('Export')),
        ('import', _('Import')),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs', verbose_name=_('User'))
    action = models.CharField(_('Action'), max_length=20, choices=ACTION_TYPES)
    
    # Generic relation to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Additional details
    description = models.TextField(_('Description'), blank=True)
    ip_address = models.GenericIPAddressField(_('IP Address'), null=True, blank=True)
    user_agent = models.TextField(_('User Agent'), blank=True)
    changes = models.JSONField(_('Changes'), null=True, blank=True)
    
    # Timestamp
    timestamp = models.DateTimeField(_('Timestamp'), default=timezone.now)

    class Meta:
        verbose_name = _('Audit Log')
        verbose_name_plural = _('Audit Logs')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"


class SystemSetting(models.Model):
    """
    System-wide settings and configurations.
    """
    key = models.CharField(_('Setting Key'), max_length=100, unique=True)
    value = models.TextField(_('Value'))
    description = models.TextField(_('Description'), blank=True)
    data_type = models.CharField(_('Data Type'), max_length=20, choices=[
        ('string', _('String')),
        ('integer', _('Integer')),
        ('boolean', _('Boolean')),
        ('json', _('JSON')),
    ], default='string')
    is_public = models.BooleanField(_('Public'), default=False)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='system_settings', verbose_name=_('Updated By'))
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('System Setting')
        verbose_name_plural = _('System Settings')
        ordering = ['key']

    def __str__(self):
        return self.key


class Notification(models.Model):
    """
    Enhanced Notification system for in-app and email notifications.
    """
    NOTIFICATION_TYPES = [
        ('info', _('Information')),
        ('success', _('Success')),
        ('warning', _('Warning')),
        ('error', _('Error')),
        ('contract_expiry', _('Contract Expiry')),
        ('payment_due', _('Payment Due')),
        ('maintenance_request', _('Maintenance Request')),
        ('document_expiry', _('Document Expiry')),
        ('budget_alert', _('Budget Alert')),
        ('system', _('System Notification')),
    ]
    
    PRIORITY_LEVELS = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('urgent', _('Urgent')),
    ]
    
    # Recipients
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('User')
    )
    
    # Content
    title = models.CharField(_('Title'), max_length=200)
    message = models.TextField(_('Message'))
    notification_type = models.CharField(
        _('Type'),
        max_length=30,
        choices=NOTIFICATION_TYPES,
        default='info'
    )
    priority = models.CharField(
        _('Priority'),
        max_length=10,
        choices=PRIORITY_LEVELS,
        default='medium'
    )
    
    # Related Object (Generic relation)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Link & Actions
    link = models.CharField(_('Link URL'), max_length=500, blank=True)
    action_label = models.CharField(_('Action Label'), max_length=100, blank=True)
    action_url = models.CharField(_('Action URL'), max_length=500, blank=True)
    
    # Status
    is_read = models.BooleanField(_('Read'), default=False)
    read_at = models.DateTimeField(_('Read At'), null=True, blank=True)
    is_sent_email = models.BooleanField(_('Email Sent'), default=False)
    email_sent_at = models.DateTimeField(_('Email Sent At'), null=True, blank=True)
    
    # Scheduling
    scheduled_for = models.DateTimeField(
        _('Scheduled For'),
        null=True,
        blank=True,
        help_text=_('Schedule notification for future delivery')
    )
    
    # Metadata
    metadata = models.JSONField(
        _('Metadata'),
        null=True,
        blank=True,
        help_text=_('Additional data as JSON')
    )
    
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', '-created_at']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
    
    def send_email(self):
        """Send notification via email"""
        if not self.is_sent_email and self.user.email:
            from django.core.mail import send_mail
            from django.conf import settings
            
            try:
                send_mail(
                    subject=self.title,
                    message=self.message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[self.user.email],
                    fail_silently=False,
                )
                self.is_sent_email = True
                self.email_sent_at = timezone.now()
                self.save()
                return True
            except Exception as e:
                print(f"Failed to send email: {e}")
                return False
        return False


class NotificationPreference(models.Model):
    """
    User preferences for notifications
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preferences',
        verbose_name=_('User')
    )
    
    # Email Preferences
    email_enabled = models.BooleanField(_('Email Notifications'), default=True)
    email_contract_expiry = models.BooleanField(_('Contract Expiry Emails'), default=True)
    email_payment_due = models.BooleanField(_('Payment Due Emails'), default=True)
    email_maintenance = models.BooleanField(_('Maintenance Emails'), default=True)
    email_document_expiry = models.BooleanField(_('Document Expiry Emails'), default=True)
    email_budget_alert = models.BooleanField(_('Budget Alert Emails'), default=True)
    
    # In-App Preferences
    inapp_enabled = models.BooleanField(_('In-App Notifications'), default=True)
    inapp_contract_expiry = models.BooleanField(_('Contract Expiry Notifications'), default=True)
    inapp_payment_due = models.BooleanField(_('Payment Due Notifications'), default=True)
    inapp_maintenance = models.BooleanField(_('Maintenance Notifications'), default=True)
    inapp_document_expiry = models.BooleanField(_('Document Expiry Notifications'), default=True)
    inapp_budget_alert = models.BooleanField(_('Budget Alert Notifications'), default=True)
    
    # Digest Settings
    daily_digest = models.BooleanField(_('Daily Digest Email'), default=False)
    weekly_digest = models.BooleanField(_('Weekly Digest Email'), default=True)
    
    # Quiet Hours
    quiet_hours_start = models.TimeField(_('Quiet Hours Start'), null=True, blank=True)
    quiet_hours_end = models.TimeField(_('Quiet Hours End'), null=True, blank=True)
    
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Notification Preference')
        verbose_name_plural = _('Notification Preferences')
    
    def __str__(self):
        return f"Preferences for {self.user.username}"
    
    def should_send_email(self, notification_type):
        """Check if email should be sent for this notification type"""
        if not self.email_enabled:
            return False
        
        type_mapping = {
            'contract_expiry': self.email_contract_expiry,
            'payment_due': self.email_payment_due,
            'maintenance_request': self.email_maintenance,
            'document_expiry': self.email_document_expiry,
            'budget_alert': self.email_budget_alert,
        }
        
        return type_mapping.get(notification_type, True)
    
    def should_show_inapp(self, notification_type):
        """Check if in-app notification should be shown"""
        if not self.inapp_enabled:
            return False
        
        type_mapping = {
            'contract_expiry': self.inapp_contract_expiry,
            'payment_due': self.inapp_payment_due,
            'maintenance_request': self.inapp_maintenance,
            'document_expiry': self.inapp_document_expiry,
            'budget_alert': self.inapp_budget_alert,
        }
        
        return type_mapping.get(notification_type, True)
