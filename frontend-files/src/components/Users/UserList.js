import React, { useState, useEffect } from 'react';
import { 
  Users as UsersIcon, 
  Eye, 
  Shield, 
  User, 
  Mail, 
  Phone,
  Search,
  Filter,
  CreditCard
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useBank } from '../../context/BankContext';
import UserProfileCard from '../Profile/UserProfileCard';
import LoadingSpinner from '../UI/LoadingSpinner';

const UserList = () => {
  const { user: currentUser } = useAuth();
  const { users, fetchUsers, loading } = useBank();
  const [selectedUserId, setSelectedUserId] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [roleFilter, setRoleFilter] = useState('all');

  useEffect(() => {
    if (currentUser?.role === 'admin') {
      fetchUsers();
    }
  }, [currentUser, fetchUsers]);

  // Filter users based on search and role
  const filteredUsers = users.filter(user => {
    const matchesSearch = 
      user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.user_id.toString().includes(searchTerm);
    
    const matchesRole = roleFilter === 'all' || user.role === roleFilter;
    
    return matchesSearch && matchesRole;
  });

  const getRoleBadgeColor = (role) => {
    switch (role?.toLowerCase()) {
      case 'admin':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'user':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  // Check if current user is admin
  if (currentUser?.role !== 'admin') {
    return (
      <div className="card text-center py-12">
        <Shield className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Access Denied</h2>
        <p className="text-gray-600">You need admin privileges to view this page.</p>
      </div>
    );
  }

  if (loading && users.length === 0) {
    return <LoadingSpinner />;
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">User Management</h1>
          <p className="text-gray-600">View and manage all registered users</p>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <UsersIcon className="h-5 w-5" />
          <span>{filteredUsers.length} users</span>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-4">
          {/* Search */}
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search by username, email, or ID..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field pl-10"
              />
            </div>
          </div>

          {/* Role Filter */}
          <div className="sm:w-48">
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <select
                value={roleFilter}
                onChange={(e) => setRoleFilter(e.target.value)}
                className="input-field pl-10 appearance-none"
              >
                <option value="all">All Roles</option>
                <option value="admin">Admin</option>
                <option value="user">User</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Users Grid */}
      {filteredUsers.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredUsers.map((user) => (
            <div key={user.user_id} className="card hover:shadow-md transition-shadow">
              {/* User Header */}
              <div className="flex items-center space-x-3 mb-4">
                <div className="h-12 w-12 bg-gradient-to-br from-banking-500 to-banking-600 rounded-full flex items-center justify-center">
                  <User className="h-6 w-6 text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900">{user.username}</h3>
                  <div className="flex items-center space-x-2">
                    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${getRoleBadgeColor(user.role)}`}>
                      <Shield className="h-3 w-3 mr-1" />
                      {user.role?.toUpperCase()}
                    </span>
                    <span className="text-xs text-gray-500">ID: {user.user_id}</span>
                  </div>
                </div>
              </div>

              {/* User Info */}
              <div className="space-y-2 mb-4">
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Mail className="h-4 w-4" />
                  <span className="truncate">{user.email}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Phone className="h-4 w-4" />
                  <span>+91 {user.mob_no}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <CreditCard className="h-4 w-4" />
                  <span>{user.accounts?.length || 0} accounts</span>
                </div>
              </div>

              {/* Account Summary */}
              {user.accounts?.length > 0 && (
                <div className="bg-gray-50 rounded-lg p-3 mb-4">
                  <p className="text-sm font-medium text-gray-900 mb-1">Total Balance</p>
                  <p className="text-lg font-bold text-banking-600">
                    ₹{user.accounts.reduce((total, acc) => total + acc.balance, 0).toLocaleString()}
                  </p>
                </div>
              )}

              {/* Footer */}
              <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                <span className="text-xs text-gray-500">
                  Joined {formatDate(user.created_at)}
                </span>
                <button
                  onClick={() => setSelectedUserId(user.user_id)}
                  className="inline-flex items-center px-3 py-1.5 text-sm font-medium text-banking-600 hover:text-banking-700 hover:bg-banking-50 rounded-lg transition-colors"
                >
                  <Eye className="h-4 w-4 mr-1" />
                  View Info
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card text-center py-12">
          <UsersIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No Users Found</h2>
          <p className="text-gray-600">
            {searchTerm || roleFilter !== 'all' 
              ? 'Try adjusting your search or filter criteria.' 
              : 'No users have been registered yet.'
            }
          </p>
        </div>
      )}

      {/* User Profile Modal */}
      {selectedUserId && (
        <UserProfileCard
          userId={selectedUserId}
          onClose={() => setSelectedUserId(null)}
        />
      )}
    </div>
  );
};

export default UserList;