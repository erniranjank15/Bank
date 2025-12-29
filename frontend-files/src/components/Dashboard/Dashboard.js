import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  CreditCard, 
  Users, 
  TrendingUp, 
  Plus,
  Eye,
  Building2,
  DollarSign
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useBank } from '../../context/BankContext';
import LoadingSpinner from '../UI/LoadingSpinner';

const Dashboard = () => {
  const { user } = useAuth();
  const { accounts, users, fetchAccounts, fetchUsers, loading } = useBank();
  const [stats, setStats] = useState({
    totalAccounts: 0,
    totalBalance: 0,
    totalUsers: 0,
    averageBalance: 0
  });

  useEffect(() => {
    fetchAccounts();
    if (user?.role === 'admin') {
      fetchUsers();
    }
  }, [user, fetchAccounts, fetchUsers]);

  useEffect(() => {
    // Calculate statistics
    const totalAccounts = accounts.length;
    const totalBalance = accounts.reduce((sum, acc) => sum + acc.balance, 0);
    const averageBalance = totalAccounts > 0 ? totalBalance / totalAccounts : 0;
    const totalUsers = users.length;

    setStats({
      totalAccounts,
      totalBalance,
      totalUsers,
      averageBalance
    });
  }, [accounts, users]);

  if (loading && accounts.length === 0) {
    return <LoadingSpinner text="Loading dashboard..." />;
  }

  const isAdmin = user?.role === 'admin';

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-banking-600 to-banking-700 rounded-xl p-6 text-white">
        <h1 className="text-2xl font-bold mb-2">
          Welcome back, {user?.username}! 👋
        </h1>
        <p className="text-banking-100">
          {isAdmin 
            ? 'Manage your banking system from this dashboard' 
            : 'Manage your accounts and transactions'
          }
        </p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-lg">
              <CreditCard className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">
                {isAdmin ? 'Total Accounts' : 'My Accounts'}
              </p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalAccounts}</p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-lg">
              <DollarSign className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Balance</p>
              <p className="text-2xl font-bold text-gray-900">
                ₹{stats.totalBalance.toLocaleString()}
              </p>
            </div>
          </div>
        </div>

        {isAdmin && (
          <div className="card">
            <div className="flex items-center">
              <div className="p-3 bg-purple-100 rounded-lg">
                <Users className="h-8 w-8 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Users</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalUsers}</p>
              </div>
            </div>
          </div>
        )}

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-yellow-100 rounded-lg">
              <TrendingUp className="h-8 w-8 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Average Balance</p>
              <p className="text-2xl font-bold text-gray-900">
                ₹{Math.round(stats.averageBalance).toLocaleString()}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Accounts */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              {isAdmin ? 'Recent Accounts' : 'My Accounts'}
            </h2>
            <Link to="/accounts" className="text-banking-600 hover:text-banking-700 text-sm font-medium">
              View All
            </Link>
          </div>
          
          {accounts.length > 0 ? (
            <div className="space-y-3">
              {accounts.slice(0, 3).map((account) => (
                <div key={account.acc_no} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-banking-100 rounded-lg">
                      <CreditCard className="h-5 w-5 text-banking-600" />
                    </div>
                    <div>
                      <p className="font-medium text-gray-900">#{account.acc_no}</p>
                      <p className="text-sm text-gray-600">{account.acc_holder_name}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-banking-600">₹{account.balance.toLocaleString()}</p>
                    <p className="text-xs text-gray-500">{account.acc_type}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <CreditCard className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500 mb-4">No accounts found</p>
              <Link to="/accounts/create" className="btn-primary">
                <Plus className="h-4 w-4 mr-2" />
                Create Account
              </Link>
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="space-y-3">
            <Link
              to="/accounts/create"
              className="flex items-center p-3 bg-banking-50 hover:bg-banking-100 rounded-lg transition-colors group"
            >
              <div className="p-2 bg-banking-600 rounded-lg group-hover:bg-banking-700 transition-colors">
                <Plus className="h-5 w-5 text-white" />
              </div>
              <div className="ml-3">
                <p className="font-medium text-gray-900">Create New Account</p>
                <p className="text-sm text-gray-600">Open a new bank account</p>
              </div>
            </Link>

            <Link
              to="/accounts"
              className="flex items-center p-3 bg-green-50 hover:bg-green-100 rounded-lg transition-colors group"
            >
              <div className="p-2 bg-green-600 rounded-lg group-hover:bg-green-700 transition-colors">
                <Eye className="h-5 w-5 text-white" />
              </div>
              <div className="ml-3">
                <p className="font-medium text-gray-900">View All Accounts</p>
                <p className="text-sm text-gray-600">Manage your accounts</p>
              </div>
            </Link>

            <Link
              to="/profile"
              className="flex items-center p-3 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors group"
            >
              <div className="p-2 bg-purple-600 rounded-lg group-hover:bg-purple-700 transition-colors">
                <Users className="h-5 w-5 text-white" />
              </div>
              <div className="ml-3">
                <p className="font-medium text-gray-900">My Profile</p>
                <p className="text-sm text-gray-600">View profile information</p>
              </div>
            </Link>

            {isAdmin && (
              <Link
                to="/users"
                className="flex items-center p-3 bg-red-50 hover:bg-red-100 rounded-lg transition-colors group"
              >
                <div className="p-2 bg-red-600 rounded-lg group-hover:bg-red-700 transition-colors">
                  <Building2 className="h-5 w-5 text-white" />
                </div>
                <div className="ml-3">
                  <p className="font-medium text-gray-900">Manage Users</p>
                  <p className="text-sm text-gray-600">Admin user management</p>
                </div>
              </Link>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;