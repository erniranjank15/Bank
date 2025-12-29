import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  CreditCard, 
  TrendingUp, 
  TrendingDown, 
  Calendar,
  MapPin,
  Building2,
  Hash,
  User,
  Edit,
  Trash2
} from 'lucide-react';
import { useBank } from '../../context/BankContext';
import { useAuth } from '../../context/AuthContext';
import TransactionModal from '../Transactions/TransactionModal';
import LoadingSpinner from '../UI/LoadingSpinner';

const AccountDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const { fetchAccount, currentAccount, loading, deleteAccount } = useBank();
  
  const [transactionModal, setTransactionModal] = useState({
    isOpen: false,
    type: 'deposit'
  });
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  useEffect(() => {
    if (id) {
      fetchAccount(parseInt(id));
    }
  }, [id, fetchAccount]);

  const handleTransaction = (type) => {
    setTransactionModal({
      isOpen: true,
      type: type
    });
  };

  const closeTransactionModal = () => {
    setTransactionModal({
      isOpen: false,
      type: 'deposit'
    });
    // Refresh account data after transaction
    if (id) {
      fetchAccount(parseInt(id));
    }
  };

  const handleDeleteAccount = async () => {
    const result = await deleteAccount(parseInt(id));
    if (result.success) {
      navigate('/accounts');
    }
    setShowDeleteConfirm(false);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading && !currentAccount) {
    return <LoadingSpinner text="Loading account details..." />;
  }

  if (!currentAccount) {
    return (
      <div className="card text-center py-12">
        <CreditCard className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Account Not Found</h2>
        <p className="text-gray-600 mb-4">The requested account could not be found.</p>
        <button
          onClick={() => navigate('/accounts')}
          className="btn-primary"
        >
          Back to Accounts
        </button>
      </div>
    );
  }

  const isOwner = user?.user_id === currentAccount.user_id;
  const isAdmin = user?.role === 'admin';
  const canTransact = isOwner || isAdmin;
  const canDelete = isAdmin;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => navigate('/accounts')}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <ArrowLeft className="h-5 w-5 text-gray-600" />
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Account Details</h1>
            <p className="text-gray-600">Account #{currentAccount.acc_no}</p>
          </div>
        </div>
        
        {canDelete && (
          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="btn-danger"
          >
            <Trash2 className="h-4 w-4 mr-2" />
            Delete Account
          </button>
        )}
      </div>

      {/* Account Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Balance Card */}
        <div className="lg:col-span-2">
          <div className="card">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-banking-100 rounded-lg">
                  <CreditCard className="h-8 w-8 text-banking-600" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Current Balance</h2>
                  <p className="text-sm text-gray-600">{currentAccount.acc_type} Account</p>
                </div>
              </div>
            </div>
            
            <div className="text-center py-8">
              <p className="text-4xl font-bold text-banking-600 mb-2">
                ₹{currentAccount.balance.toLocaleString()}
              </p>
              <p className="text-gray-600">Available Balance</p>
            </div>

            {/* Transaction Buttons */}
            {canTransact && (
              <div className="flex space-x-4 pt-6 border-t border-gray-200">
                <button
                  onClick={() => handleTransaction('deposit')}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center"
                >
                  <TrendingUp className="h-5 w-5 mr-2" />
                  Deposit
                </button>
                <button
                  onClick={() => handleTransaction('withdraw')}
                  className="flex-1 bg-red-600 hover:bg-red-700 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200 flex items-center justify-center"
                  disabled={currentAccount.balance <= 0}
                >
                  <TrendingDown className="h-5 w-5 mr-2" />
                  Withdraw
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="space-y-4">
          {/* Account Status */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Account Status</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Status</span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Active
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Account Type</span>
                <span className="text-sm font-medium text-gray-900">{currentAccount.acc_type}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Minimum Balance</span>
                <span className="text-sm font-medium text-gray-900">₹100</span>
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Account Age</span>
                <span className="text-sm font-medium text-gray-900">
                  {Math.floor((new Date() - new Date(currentAccount.created_at)) / (1000 * 60 * 60 * 24))} days
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Last Updated</span>
                <span className="text-sm font-medium text-gray-900">Today</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Account Information */}
      <div className="card">
        <div className="card-header">
          <h2 className="text-xl font-semibold text-gray-900">Account Information</h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <User className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Account Holder</p>
                <p className="text-sm text-gray-600">{currentAccount.acc_holder_name}</p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <div className="p-2 bg-green-100 rounded-lg">
                <Hash className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Account Number</p>
                <p className="text-sm text-gray-600">{currentAccount.acc_no}</p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Building2 className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">IFSC Code</p>
                <p className="text-sm text-gray-600">{currentAccount.ifsc_code}</p>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <MapPin className="h-5 w-5 text-yellow-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Address</p>
                <p className="text-sm text-gray-600">{currentAccount.acc_holder_address}</p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <div className="p-2 bg-red-100 rounded-lg">
                <Calendar className="h-5 w-5 text-red-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Date of Birth</p>
                <p className="text-sm text-gray-600">{currentAccount.dob}</p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <div className="p-2 bg-indigo-100 rounded-lg">
                <Building2 className="h-5 w-5 text-indigo-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">Branch</p>
                <p className="text-sm text-gray-600">{currentAccount.branch}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gray-100 rounded-lg">
              <Calendar className="h-5 w-5 text-gray-600" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900">Account Created</p>
              <p className="text-sm text-gray-600">{formatDate(currentAccount.created_at)}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Transaction Modal */}
      <TransactionModal
        isOpen={transactionModal.isOpen}
        onClose={closeTransactionModal}
        accountId={currentAccount.acc_no}
        accountBalance={currentAccount.balance}
        accountHolder={currentAccount.acc_holder_name}
        transactionType={transactionModal.type}
      />

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-red-100 rounded-lg">
                <Trash2 className="h-6 w-6 text-red-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Delete Account</h3>
                <p className="text-sm text-gray-600">This action cannot be undone</p>
              </div>
            </div>
            
            <p className="text-gray-700 mb-6">
              Are you sure you want to delete account #{currentAccount.acc_no}? 
              This will permanently remove the account and all associated data.
            </p>
            
            <div className="flex space-x-3">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="flex-1 btn-secondary"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteAccount}
                className="flex-1 btn-danger"
              >
                Delete Account
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AccountDetails;