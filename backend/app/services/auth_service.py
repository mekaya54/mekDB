from typing import Dict


def authenticate(email: str, password: str) -> Dict:
	user = {
		"username": email.split("@")[0],
		"email": email,
		"avatarUrl": f"https://api.dicebear.com/7.x/avataaars/svg?seed={email}",
	}
	token = "dev-token"
	return {"user": user, "token": token}


def register(email: str, password: str) -> Dict:
	return authenticate(email, password)
