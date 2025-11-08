# 📨 خطة نظام المراسلات الداخلية والمستخدمين المتصلين
## Origin App - Real Estate Management System

---

## 🎯 **الهدف**
إضافة نظام مراسلات داخلي ونظام تتبع المستخدمين المتصلين حالياً للنظام.

---

## 📋 **المتطلبات**

### **1. نظام المستخدمين المتصلين** 👥

#### **Features**:
- ✅ تتبع المستخدمين المتصلين حالياً (Online Users)
- ✅ عرض آخر نشاط للمستخدم (Last Activity)
- ✅ عداد المستخدمين المتصلين
- ✅ قائمة بالمستخدمين النشطين
- ✅ حالة المستخدم (Online/Offline/Away)

#### **Implementation**:
```python
# Model: UserActivity
- user (FK to User)
- last_activity (DateTime)
- ip_address
- user_agent
- is_online (Boolean)
- status (online/offline/away)

# Middleware: OnlineUsersMiddleware
- تحديث last_activity عند كل request
- تحديد Online إذا آخر نشاط < 5 دقائق
- تحديد Away إذا آخر نشاط < 15 دقيقة
- تحديد Offline إذا آخر نشاط > 15 دقيقة
```

#### **Views**:
```python
- online_users_list() - قائمة المستخدمين المتصلين
- user_status_api() - API للحصول على حالة مستخدم
- online_count_api() - API لعدد المتصلين
```

---

### **2. نظام المراسلات الداخلية** 📨

#### **Features**:
- ✅ إرسال رسائل بين المستخدمين
- ✅ صندوق الوارد (Inbox)
- ✅ صندوق الصادر (Sent)
- ✅ رسائل غير مقروءة (Unread Badge)
- ✅ الرد على الرسائل
- ✅ حذف الرسائل
- ✅ البحث في الرسائل
- ✅ إرفاق ملفات (اختياري)
- ✅ إشعار عند استلام رسالة جديدة

#### **Models**:
```python
# Message Model
- sender (FK to User)
- recipient (FK to User)
- subject (CharField)
- body (TextField)
- is_read (Boolean)
- read_at (DateTime)
- parent_message (FK to self) - للردود
- attachment (FileField) - اختياري
- created_at (DateTime)
- updated_at (DateTime)

# MessageAttachment Model (اختياري)
- message (FK to Message)
- file (FileField)
- file_name (CharField)
- file_size (Integer)
- uploaded_at (DateTime)
```

#### **Views**:
```python
# Inbox & Sent
- message_inbox() - صندوق الوارد
- message_sent() - صندوق الصادر
- message_compose() - إنشاء رسالة جديدة
- message_detail() - عرض رسالة
- message_reply() - الرد على رسالة
- message_delete() - حذف رسالة
- message_mark_read() - تحديد كمقروءة
- message_search() - البحث

# API Endpoints
- message_unread_count() - عدد الرسائل غير المقروءة
- message_new_notification() - إشعار برسالة جديدة
```

#### **Templates**:
```html
- messages/inbox.html - صندوق الوارد
- messages/sent.html - صندوق الصادر
- messages/compose.html - إنشاء رسالة
- messages/detail.html - عرض رسالة
- messages/reply.html - الرد
```

---

## 🎨 **التصميم المقترح**

### **صفحة المستخدمين المتصلين**:
```
┌─────────────────────────────────────┐
│  👥 Online Users (5)                │
├─────────────────────────────────────┤
│  🟢 Ahmed Hassan                    │
│     Last activity: 2 minutes ago    │
├─────────────────────────────────────┤
│  🟢 Sarah Mohamed                   │
│     Last activity: Just now         │
├─────────────────────────────────────┤
│  🟡 Zakee Tahawi (Away)            │
│     Last activity: 10 minutes ago   │
├─────────────────────────────────────┤
│  🔴 Omar Ali (Offline)             │
│     Last activity: 1 hour ago       │
└─────────────────────────────────────┘
```

### **صفحة الرسائل**:
```
┌─────────────────────────────────────┐
│  📨 Messages                         │
│  ┌─────┬─────┬─────┬──────┐        │
│  │Inbox│Sent │New  │Search│        │
│  └─────┴─────┴─────┴──────┘        │
├─────────────────────────────────────┤
│  📩 New Message (5)                 │
├─────────────────────────────────────┤
│  🔵 Ahmed Hassan                    │
│     Re: Property #123              │
│     2 minutes ago                  │
├─────────────────────────────────────┤
│  ⚪ Sarah Mohamed                   │
│     Contract Update                │
│     1 hour ago (Read)              │
└─────────────────────────────────────┘
```

---

## 📐 **Database Schema**

### **UserActivity Table**:
```sql
CREATE TABLE user_activity (
    id INT PRIMARY KEY,
    user_id INT FK,
    last_activity DATETIME,
    ip_address VARCHAR(45),
    user_agent TEXT,
    is_online BOOLEAN,
    status VARCHAR(20),
    created_at DATETIME,
    updated_at DATETIME
);

INDEX idx_user_id ON user_activity(user_id);
INDEX idx_last_activity ON user_activity(last_activity);
INDEX idx_is_online ON user_activity(is_online);
```

### **Message Table**:
```sql
CREATE TABLE internal_message (
    id INT PRIMARY KEY,
    sender_id INT FK,
    recipient_id INT FK,
    subject VARCHAR(200),
    body TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    read_at DATETIME NULL,
    parent_message_id INT FK NULL,
    attachment VARCHAR(255) NULL,
    created_at DATETIME,
    updated_at DATETIME
);

INDEX idx_sender ON internal_message(sender_id);
INDEX idx_recipient ON internal_message(recipient_id);
INDEX idx_is_read ON internal_message(is_read);
INDEX idx_created_at ON internal_message(created_at);
```

---

## 🔧 **Implementation Steps**

### **Phase 1: Online Users System** (30 min)
```
✅ 1. Create UserActivity model
✅ 2. Create OnlineUsersMiddleware
✅ 3. Create online_users views
✅ 4. Create templates
✅ 5. Update URLs
✅ 6. Add to sidebar menu
✅ 7. Test functionality
```

### **Phase 2: Messaging System** (60 min)
```
✅ 1. Create Message model
✅ 2. Create MessageAttachment model (optional)
✅ 3. Run migrations
✅ 4. Create messaging views (inbox, sent, compose, etc.)
✅ 5. Create templates
✅ 6. Update URLs
✅ 7. Add message icon to navbar with unread badge
✅ 8. Integrate with notification system
✅ 9. Test sending/receiving messages
```

### **Phase 3: Integration & Polish** (30 min)
```
✅ 1. Add auto-refresh for new messages
✅ 2. Add notification sound (optional)
✅ 3. Add search functionality
✅ 4. Style improvements
✅ 5. Mobile responsiveness
✅ 6. Documentation
```

---

## 🎯 **Priority Features**

### **Must Have** (MVP):
- ✅ Send/receive messages
- ✅ Inbox & Sent folders
- ✅ Unread badge
- ✅ Mark as read
- ✅ Delete messages
- ✅ Online users list
- ✅ Last activity tracking

### **Nice to Have** (Future):
- ⏸️ File attachments
- ⏸️ Message threads
- ⏸️ Group messages
- ⏸️ Message templates
- ⏸️ Email notifications
- ⏸️ Advanced search
- ⏸️ Message archiving

---

## 🔌 **API Endpoints**

### **Online Users**:
```
GET  /api/users/online/          - List online users
GET  /api/users/online/count/    - Count online users
GET  /api/users/status/<id>/     - Get user status
```

### **Messages**:
```
GET  /messages/                   - Inbox
GET  /messages/sent/              - Sent messages
GET  /messages/compose/           - New message form
POST /messages/send/              - Send message
GET  /messages/<id>/              - View message
POST /messages/<id>/reply/        - Reply to message
POST /messages/<id>/delete/       - Delete message
POST /messages/<id>/read/         - Mark as read
GET  /api/messages/unread/        - Unread count
```

---

## 📱 **UI Components**

### **Navbar Updates**:
```html
<!-- Messages Icon -->
<a href="/messages/" class="position-relative">
    <i class="fas fa-envelope"></i>
    <span class="badge bg-danger">3</span>
</a>

<!-- Online Users -->
<a href="/users/online/">
    <i class="fas fa-users"></i>
    <span class="badge bg-success">5</span>
</a>
```

### **Sidebar Updates**:
```html
<li>
    <a href="/messages/">
        <i class="fas fa-envelope"></i>
        Messages
        <span class="badge bg-danger">3</span>
    </a>
</li>

<li>
    <a href="/users/online/">
        <i class="fas fa-circle text-success"></i>
        Online Users (5)
    </a>
</li>
```

---

## 🧪 **Testing Checklist**

### **Online Users**:
- [ ] User appears online after login
- [ ] User appears offline after 15 min inactivity
- [ ] Away status after 5 min inactivity
- [ ] Count updates in real-time
- [ ] List refreshes automatically

### **Messages**:
- [ ] Send message successfully
- [ ] Receive message in inbox
- [ ] Unread badge appears
- [ ] Mark as read works
- [ ] Delete message works
- [ ] Reply functionality works
- [ ] Search finds messages
- [ ] Pagination works

---

## 📊 **Performance Considerations**

### **Optimization**:
```python
# Cache online users count
cache.set('online_users_count', count, 60)  # 1 min cache

# Use select_related for messages
Message.objects.select_related('sender', 'recipient')

# Index important fields
class Meta:
    indexes = [
        models.Index(fields=['is_read', 'recipient']),
        models.Index(fields=['created_at']),
    ]
```

---

## 🔒 **Security Considerations**

### **Permissions**:
```python
# Only logged-in users can access
@login_required

# Users can only read their own messages
if message.recipient != request.user:
    return HttpResponseForbidden()

# Sanitize message content
from django.utils.html import escape
body = escape(request.POST.get('body'))
```

---

## 📝 **Next Steps**

### **After Implementation**:
1. ✅ Test all features thoroughly
2. ✅ Update documentation
3. ✅ Create migration files
4. ✅ Add to admin panel
5. ✅ Git commit changes
6. ✅ Push to GitHub

---

## 🎊 **Expected Outcome**

```
✨ Complete Internal Messaging System
✨ Real-time Online Users Tracking
✨ Professional UI/UX
✨ Fully Integrated with Notifications
✨ Mobile Responsive
✨ Production Ready
```

---

**Status**: Ready for Implementation  
**Estimated Time**: 2 hours  
**Priority**: High  
**Complexity**: Medium  

---

**Developer**: Zakee Tahawi  
**Date**: November 8, 2025  
**Project**: Origin App Real Estate Management System
