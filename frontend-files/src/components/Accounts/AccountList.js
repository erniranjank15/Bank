import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  CreditCard, 
  Plus, 
  Eye, 
  TrendingUp, 
  TrendingDown,
  Search,
  Filter,
  Building2
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useBank } from '../../context/BankContext';
import TransactionModal from '../Transactions/TransactionModal';
import LoadingSpinner from '../UI/LoadingSpinner';

const AccountList = () => {
  const { user } = useAuth();
  const { accounts, fetchAccounts, loading } = useBank();
  const [searchTerm, setSearchTerm] = useState('');
  const [typeFilter, setTypeFilter] = useState('all');
  const [transactionModal, setTransactionModal] = useState({
    isOpen: false,
    accountId: null,
    accountBalance: 0,
    accountHolder: '',
    type: 'deposit'
  });

  useEffect(() => {
    fetchAccounts();
  }, [fetchAccounts]);

  // Filter accounts based on search and type
  const filteredAccounts = accounts.filter(account => {
    const matchesSearch = 
      account.acc_holder_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      account.acc_no.toString().includes(searchTerm) ||
      account.acc_type.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesType = typeFilter === 'all' || account.acc_type.toLowerCase() === typeFilter.toLowerCase();
    
    return matchesSearch && matchesType;
  });

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
    // Refresh accounts after transaction
    fetchAccounts();
  };

  const getAccountTypeColor = (type) => {
    switch (type?.toLowerCase()) {
      case 'savings':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'current':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'fixed':
        return 'bg-purple-100 text-purple-800 border-purple-200';
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

  if (loading && accounts.length === 0) {
    return <LoadingSpinner text="Loading accounts..." />;
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Bank Accounts</h1>
          <p className="text-gray-600">
            {user?.role === 'admin' ? 'Manage all bank accounts' : 'Manage your bank accounts'}
          </p>
        </div>
        <Link to="/accounts/create" className="btn-primary">
          <Plus className="h-5 w-5 mr-2" />
          New Account
        </Link>
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
                placeholder="Search by account holder, number, or type..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field pl-10"
              />
            </div>
          </div>

          {/* Type Filter */}
          <div className="sm:w-48">
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <select
                value={typeFilter}
                onChange={(e) => setTypeFilter(e.target.value)}
                className="input-field pl-10 appearance-none"
              >
                <option value="all">All Types</option>
                <option value="savings">Savings</option>
                <option value="current">Current</option>
                <option value="fixed">Fixed Deposit</option>
              </select>
            </div>
          </div>
        </div>

        {/* Summary Stats */}
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-banking-600">{filteredAccounts.length}</p>
              <p className="text-sm text-gray-600">Total Accounts</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">
                ₹{filteredAccounts.reduce((sum, acc) => sum + acc.balance, 0).toLocaleString()}
              </p>
              <p className="text-sm text-gray-600">Total Balance</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">
                ₹{filteredAccounts.length > 0 ? Math.round(filteredAccounts.reduce((sum, acc) => sum + acc.balance, 0) / filteredAccounts.length).toLocaleString() : 0}
              </p>
              <p className="text-sm text-gray-600">Average Balance</p>
            </div>
          </div>
        </div>
      </div>

      {/* Accounts Grid */}
      {filteredAccounts.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAccounts.map((account) => (
            <div key={account.acc_no} className="card hover:shadow-md transition-shadow">
              {/* Account Header */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-banking-100 rounded-lg">
                    <CreditCard className="h-6 w-6 text-banking-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">#{account.acc_no}</h3>
                    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${getAccountTypeColor(account.acc_type)}`}>
                      {account.acc_type}
                    </span>
                  </div>
                </div>
              </div>

              {/* Account Info */}
              <div className="space-y-2 mb-4">
                <div>
                  <p className="text-sm font-medium text-gray-900">{account.acc_holder_name}</p>
                  <p className="text-xs text-gray-600">{account.acc_holder_address}</p>
                </div>
                <div className="flex items-center space-x-2 text-xs text-gray-600">
                  <Building2 className="h-3 w-3" />
                  <span>IFSC: {account.ifsc_code}</span>
                  <span>•</span>
                  <span>{account.branch}</span>
                </div>
              </div>

              {/* Balance */}
              <div className="bg-gray-50 rounded-lg p-3 mb-4">
                <p className="text-sm text-gray-600 mb-1">Current Balance</p>
                <p className="text-xl font-bold text-banking-600">
                  ₹{account.balance.toLocaleString()}
                </p>
              </div>

              {/* Action Buttons */}
              <div className="space-y-2">
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleTransaction(account, 'deposit')}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white text-sm font-medium py-2 px-3 rounded-lg transition-colors flex items-center justify-center"
                  >
                    <TrendingUp className="h-4 w-4 mr-1" />
                    Deposit
                  </button>
                  <button
                    onClick={() => handleTransaction(account, 'withdraw')}
                    className="flex-1 bg-red-600 hover:bg-red-700 text-white text-sm font-medium py-2 px-3 rounded-lg transition-colors flex items-center justify-center"
                    disabled={account.balance <= 0}
                  >
                    <TrendingDown className="h-4 w-4 mr-1" />
                    Withdraw
                  </button>
                </div>
                
                <Link
                  to={`/accounts/${account.acc_no}`}
                  className="w-full btn-secondary text-center flex items-center justify-center"
                >
                  <Eye className="h-4 w-4 mr-2" />
                  View Details
                </Link>
              </div>

              {/* Footer */}
              <div className="mt-4 pt-4 border-t border-gray-200">
                <p className="text-xs text-gray-500">
                  Created {formatDate(account.created_at)}
                </p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card text-center py-12">
          <CreditCard className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No Accounts Found</h2>
          <p className="text-gray-600 mb-4">
            {searchTerm || typeFilter !== 'all' 
              ? 'Try adjusting your search or filter criteria.' 
              : 'Create your first bank account to get started.'
            }
          </p>
          {(!searchTerm && typeFilter === 'all') && (
            <Link to="/accounts/create" className="btn-primary">
              <Plus className="h-5 w-5 mr-2" />
              Create Account
            </Link>
          )}
        </div>
      )}

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

export default AccountList;