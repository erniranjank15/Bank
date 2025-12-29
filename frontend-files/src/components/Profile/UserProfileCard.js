import React, { useState, useEffect } from 'react';
import { 
  User, 
  Mail, 
  Phone, 
  Calendar, 
  Shield, 
  CreditCard, 
  Eye,
  X,
  Building2,
  TrendingUp,
  TrendingDown
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useBank } from '../../context/BankContext';
import TransactionModal from '../Transactions/TransactionModal';
import LoadingSpinner from '../UI/LoadingSpinner';

const UserProfileCard = ({ userId = null, onClose = null }) => {
  const { user: currentUser } = useAuth();
  const { fetchUserProfile, loading } = useBank();
  const [userProfile, setUserProfile] = useState(null);
  const [profileLoading, setProfileLoading] = useState(false);
  const [transactionModal, setTransactionModal] = useState({
    isOpen: false,
    accountId: null,
    accountBalance: 0,
    accountHolder: '',
    type: 'deposit'
  });

  // Determine which user to show
  const targetUserId = userId || currentUser?.user_id;
  const isModal = !!onClose; // If onClose is provided, it's a modal
  const canTransact = currentUser?.user_id === userProfile?.user_id || currentUser?.role === 'admin';

  useEffect(() => {
    const loadUserProfile = async () => {
      if (targetUserId) {
        setProfileLoading(true);
        const result = await fetchUserProfile(targetUserId);
        if (result.success) {
          setUserProfile(result.data);
        }
        setProfileLoading(false);
      }
    };

    loadUserProfile();
  }, [targetUserId, fetchUserProfile]);

  const handleTransaction = (account, type) => {
    setTransactionModal({
      isOpen: true,
      accountId: account.acc_no,
      accountBalance: account.balance,
      accountHolder: account.acc_holder_name,
      type: type
    });
  };

  const closeTransactionModal = () => {
    setTransactionModal({
      isOpen: false,
      accountId: null,
      accountBalance: 0,
      accountHolder: '',
      type: 'deposit'
    });
    // Refresh profile data after transaction
    if (targetUserId) {
      const loadUserProfile = async () => {
        setProfileLoading(true);
        const result = await fetchUserProfile(targetUserId);
        if (result.success) {
          setUserProfile(result.data);
        }
        setProfileLoading(false);
      };
      loadUserProfile();
    }
  };

  if (profileLoading || loading) {
    return (
      <div className={`${isModal ? 'p-8' : ''} flex justify-center items-center`}>
        <LoadingSpinner />
      </div>
    );
  }

  if (!userProfile) {
    return (
      <div className={`${isModal ? 'p-8' : 'card'} text-center`}>
        <p className="text-gray-500">User profile not found</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

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

  const ProfileContent = () => (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="h-16 w-16 bg-gradient-to-br from-banking-500 to-banking-600 rounded-full flex items-center justify-center">
            <User className="h-8 w-8 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{userProfile.username}</h2>
            <div className="flex items-center space-x-2 mt-1">
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getRoleBadgeColor(userProfile.role)}`}>
                <Shield className="h-3 w-3 mr-1" />
                {userProfile.role?.toUpperCase()}
              </span>
              <span className="text-sm text-gray-500">ID: {userProfile.user_id}</span>
            </div>
          </div>
        </div>
        {isModal && (
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        )}
      </div>

      {/* Contact Information */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 border-b border-gray-200 pb-2">
            Contact Information
          </h3>
          
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Mail className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900">Email</p>
              <p className="text-sm text-gray-600">{userProfile.email}</p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <Phone className="h-5 w-5 text-green-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900">Mobile Number</p>
              <p className="text-sm text-gray-600">+91 {userProfile.mob_no}</p>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Calendar className="h-5 w-5 text-purple-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900">Member Since</p>
              <p className="text-sm text-gray-600">{formatDate(userProfile.created_at)}</p>
            </div>
          </div>
        </div>

        {/* Account Summary */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 border-b border-gray-200 pb-2">
            Account Summary
          </h3>
          
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-banking-100 rounded-lg">
              <CreditCard className="h-5 w-5 text-banking-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900">Total Accounts</p>
              <p className="text-sm text-gray-600">{userProfile.accounts?.length || 0} accounts</p>
            </div>
          </div>

          {userProfile.accounts?.length > 0 && (
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <Building2 className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Total Balance</p>
                <p className="text-sm text-gray-600">
                  ₹{userProfile.accounts.reduce((total, acc) => total + acc.balance, 0).toLocaleString()}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Accounts List */}
      {userProfile.accounts?.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 border-b border-gray-200 pb-2">
            Bank Accounts
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {userProfile.accounts.map((account) => (
              <div key={account.acc_no} className="bg-gray-50 rounded-lg p-4 border">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <p className="font-medium text-gray-900">Account #{account.acc_no}</p>
                    <p className="text-sm text-gray-600">{account.acc_type}</p>
                  </div>
                  <span className="text-lg font-bold text-banking-600">
                    ₹{account.balance.toLocaleString()}
                  </span>
                </div>
                <div className="text-xs text-gray-500 space-y-1 mb-3">
                  <p>Holder: {account.acc_holder_name}</p>
                  <p>IFSC: {account.ifsc_code}</p>
                  <p>Branch: {account.branch}</p>
                </div>
                
                {/* Quick Transaction Buttons */}
                {canTransact && (
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleTransaction(account, 'deposit')}
                      className="flex-1 bg-green-600 hover:bg-green-700 text-white text-xs font-medium py-1.5 px-2 rounded transition-colors flex items-center justify-center"
                    >
                      <TrendingUp className="h-3 w-3 mr-1" />
                      Deposit
                    </button>
                    <button
                      onClick={() => handleTransaction(account, 'withdraw')}
                      className="flex-1 bg-red-600 hover:bg-red-700 text-white text-xs font-medium py-1.5 px-2 rounded transition-colors flex items-center justify-center"
                      disabled={account.balance <= 0}
                    >
                      <TrendingDown className="h-3 w-3 mr-1" />
                      Withdraw
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No Accounts Message */}
      {userProfile.accounts?.length === 0 && (
        <div className="text-center py-8 bg-gray-50 rounded-lg">
          <CreditCard className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">No bank accounts found</p>
          <p className="text-sm text-gray-400">Create your first account to get started</p>
        </div>
      )}
    </div>
  );

  // Return modal version if onClose is provided
  if (isModal) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-xl shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
          <div className="p-6">
            <ProfileContent />
          </div>
        </div>
        
        {/* Transaction Modal */}
        <TransactionModal
          isOpen={transactionModal.isOpen}
          onClose={closeTransactionModal}
          accountId={transactionModal.accountId}
          accountBalance={transactionModal.accountBalance}
          accountHolder={transactionModal.accountHolder}
          transactionType={transactionModal.type}
        />
      </div>
    );
  }

  // Return card version for regular display
  return (
    <div>
      <div className="card">
        <ProfileContent />
      </div>
      
      {/* Transaction Modal */}
      <TransactionModal
        isOpen={transactionModal.isOpen}
        onClose={closeTransactionModal}
        accountId={transactionModal.accountId}
        accountBalance={transactionModal.accountBalance}
        accountHolder={transactionModal.accountHolder}
        transactionType={transactionModal.type}
      />
    </div>
  );
};

export default UserProfileCard;