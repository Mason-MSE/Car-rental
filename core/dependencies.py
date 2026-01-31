from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from core.security import decode_access_token
from fastapi.routing import compile_path



from sqlalchemy.orm import Session
from database import get_db
from models.user import UserModel
from models.resource import ResourceModel
from models.role_resource import RoleResourceModel
from models.user_role import UserRoleModel  # adjust import


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserModel:
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# ---------------- Permission checker ----------------
def require_permission():
    """
    Dependency to check if current user has permission for this request
    """
    def checker(request: Request, current_user: UserModel = Depends(get_current_user),
                db: Session = Depends(get_db)):
        path = request.url.path
        method = request.method.upper()
        print(current_user.status)
     
        # Get user roles
        role_ids = db.query(UserRoleModel.role_id).filter(
            UserRoleModel.user_id == current_user.id
        ).all()
        role_ids = [r[0] for r in role_ids]

        if  not role_ids:
            raise HTTPException(status_code=403, detail="No roles assigned")

        # Get role resources
        resources = db.query(ResourceModel.resource_link, ResourceModel.resource_method)\
            .join(RoleResourceModel, RoleResourceModel.resource_id == ResourceModel.id)\
            .filter(RoleResourceModel.role_id.in_(role_ids))\
            .all()
        
        # print(f"Resources for roles: {resources} res_path: {path} res_method: {method}")

        # Check if current path + method matches any resource
        for res_path, res_method in resources:
            path_regex, _, param_convertors =compile_path(res_path)
            if path_regex.match(path) and res_method.upper() == method:
                return current_user

        # Deny if no match
        raise HTTPException(status_code=403, detail="Permission denied")
    return checker