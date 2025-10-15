from django.db import models
import uuid

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ✅ add default
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=150, blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    subscribe = models.BooleanField(default=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username or self.email
    

# 🏠 Server (Guild)
class Server(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    image_url = models.TextField(blank=True, null=True)
    invite_code = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_servers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["owner"])]

    def __str__(self):
        return self.name


# 👥 Member (User inside a Server)
class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="members")
    nickname = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=50, default="Member")
    joined_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "server")

    def __str__(self):
        return f"{self.user.username} in {self.server.name}"


# 💬 Channel (Text or Voice)
class Channel(models.Model):
    CHANNEL_TYPES = (
        ("text", "Text"),
        ("voice", "Voice"),
        ("video", "Video"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="channels")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CHANNEL_TYPES, default="text")
    topic = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.server.name})"


# 💭 Message (Live Chat)
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField(blank=True, null=True)
    attachment_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"