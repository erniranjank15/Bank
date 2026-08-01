import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status

from models import Users, PasswordResetOTP
from schemas import ForgotPasswordRequest, VerifyOTPRequest, ResetPasswordRequest
from security import get_password_hash
from service.emailService import send_email

router = APIRouter(prefix="/forgot-password", tags=["Forgot Password"])

OTP_EXPIRY_MINUTES = 10


# ── 1. Request OTP ──────────────────────────────────────────────────────────────

@router.post("/request-otp", status_code=status.HTTP_200_OK)
async def request_otp(request: ForgotPasswordRequest):
    """
    Step 1 – Send a 6-digit OTP to the user's registered email.
    Always returns a generic success message to prevent email enumeration.
    """
    user = await Users.find_one(Users.email == request.email)

    if user:
        # Delete any previously pending OTPs for this email (prevent spam)
        await PasswordResetOTP.find(PasswordResetOTP.email == request.email).delete()

        # Generate a cryptographically secure 6-digit OTP
        otp_code = str(secrets.randbelow(900000) + 100000)  # 100000 – 999999

        otp_record = PasswordResetOTP(
            email=request.email,
            otp=otp_code,
            expires_at=datetime.utcnow() + timedelta(minutes=OTP_EXPIRY_MINUTES),
        )
        await otp_record.insert()

        # Build a nice HTML email
        email_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 480px; margin: auto;
                    border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
            <div style="background: #1a3c5e; padding: 24px; text-align: center;">
                <h2 style="color: #ffffff; margin: 0;">NK Bank</h2>
                <p style="color: #90caf9; margin: 4px 0 0;">Password Reset Request</p>
            </div>
            <div style="padding: 32px;">
                <p style="font-size: 15px; color: #333;">Hello <strong>{user.username}</strong>,</p>
                <p style="font-size: 15px; color: #333;">
                    We received a request to reset your password.
                    Use the OTP below to proceed. It is valid for
                    <strong>{OTP_EXPIRY_MINUTES} minutes</strong>.
                </p>
                <div style="text-align: center; margin: 32px 0;">
                    <span style="display: inline-block; font-size: 36px; font-weight: bold;
                                 letter-spacing: 10px; color: #1a3c5e; background: #e8f0fe;
                                 padding: 16px 32px; border-radius: 8px;">
                        {otp_code}
                    </span>
                </div>
                <p style="font-size: 13px; color: #888;">
                    If you did not request a password reset, you can safely ignore this email.
                    Your account remains secure.
                </p>
            </div>
            <div style="background: #f5f5f5; padding: 16px; text-align: center;
                        font-size: 12px; color: #aaa;">
                &copy; 2025 NK Bank. All rights reserved.
            </div>
        </div>
        """

        await send_email(
            recipient=request.email,
            subject="NK Bank – Your Password Reset OTP",
            body=email_body,
        )

    # Always return the same message regardless of whether the email exists
    return {"message": "If this email is registered, an OTP has been sent to it."}


# ── 2. Verify OTP ───────────────────────────────────────────────────────────────

@router.post("/verify-otp", status_code=status.HTTP_200_OK)
async def verify_otp(request: VerifyOTPRequest):
    """
    Step 2 – Verify that the OTP is correct and has not expired or been used.
    Does NOT mark the OTP as used (that happens at reset step).
    """
    otp_record = await PasswordResetOTP.find_one(
        PasswordResetOTP.email == request.email,
        PasswordResetOTP.otp == request.otp,
    )

    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP.",
        )

    if otp_record.is_used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This OTP has already been used.",
        )

    if datetime.utcnow() > otp_record.expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired. Please request a new one.",
        )

    return {"message": "OTP verified successfully. You may now reset your password."}


# ── 3. Reset Password ──────────────────────────────────────────────────────────

@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(request: ResetPasswordRequest):
    """
    Step 3 – Reset the user's password after OTP re-validation.
    Marks the OTP as used so it cannot be replayed.
    """
    otp_record = await PasswordResetOTP.find_one(
        PasswordResetOTP.email == request.email,
        PasswordResetOTP.otp == request.otp,
    )

    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP.",
        )

    if otp_record.is_used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This OTP has already been used.",
        )

    if datetime.utcnow() > otp_record.expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired. Please request a new one.",
        )

    # Find the user
    user = await Users.find_one(Users.email == request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    # Update the password
    user.hashed_password = get_password_hash(request.new_password)
    await user.save()

    # Invalidate the OTP so it cannot be reused
    otp_record.is_used = True
    await otp_record.save()

    return {"message": "Password reset successfully. You can now log in with your new password."}
