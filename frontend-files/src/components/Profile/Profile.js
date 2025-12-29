import React from 'react';
import { useAuth } from '../../context/AuthContext';
import UserProfileCard from './UserProfileCard';

const Profile = () => {
  const { user } = useAuth();

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Profile</h1>
          <p className="text-gray-600">View and manage your account information</p>
        </div>
      </div>

      {/* Profile Card */}
      <UserProfileCard userId={user?.user_id} />
    </div>
  );
};

export default Profile;