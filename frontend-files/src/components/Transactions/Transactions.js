import React, { useState, useEffect } from 'react';
import { 
  ArrowRightLeft, 
  TrendingUp, 
  TrendingDown, 
  Calendar,
  CreditCard,
  Filter,
  Search
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useBank } from '../../context/BankContext';
import LoadingSpinner from '../UI/LoadingSpinner';

const Transactions = () => {
  const { user } = useAuth();
  const { accounts, fetchAccounts, loading } = useBank();
  const [searchTerm, setSearchTerm] = useState('');
  const [accountFilter, setAccountFilter] = useState('all');

  useEffect(() => {
    fetchAccounts();
  }, [fetchAccounts]);

  // Mock transaction data - In a real app, this would come from an API
  const mockTransactions = [
    {
      id: 1,
      type: 'deposit',
      amount: 5000,
      account_no: 1,
      account_holder: 'John Doe',
      date: '2024-01-15T10:30:00Z',
      description: 'Cash Deposit',
      balance_after: 15000
    },
    {
      id: 2,
      type: 'withdraw',
      amount: 2000,
      account_no: 1,
      account_holder: 'John Doe',
      date: '2024-01-14T14:20:00Z',
      description: 'ATM Withdrawal',
      balance_after: 10000
    },
    {
      id: 3,
      type: 'deposit',
      amount: 3000,
      account_no: 2,
      account_holder: 'Jane Smith',
      date: '2024-01-13T09:15:00Z',
      description: 'Online Transfer',
      balance_after: 8000
    },
  ];

  const filteredTransactions = mockTransactions.filter(transaction => {
    const matchesSearch = 
      transaction.account_holder.toLowerCase().includes(searchTerm.toLowerCase()) ||
      transaction.account_no.toString().includes(searchTerm) ||
      transaction.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesAccount = accountFilter === 'all' || transaction.account_no.toString() === accountFilter;
    
    return matchesSearch && matchesAccount;
  });

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getTransactionIcon = (type) => {
    return type === 'deposit' ? TrendingUp : TrendingDown;
  };

  const getTransactionColor = (type) => {
    return type === 'deposit' 
      ? 'text-green-600 bg-green-100' 
      : 'text-red-600 bg-red-100';
  };

  if (loading && accounts.length === 0) {
    return <LoadingSpinner text="Loading transactions..." />;
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Transaction History</h1>
          <p className="text-gray-600">
            {user?.role === 'admin' ? 'View all system transactions' : 'View your transaction history'}
          </p>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-600">
          <ArrowRightLeft className="h-5 w-5" />
          <span>{filteredTransactions.length} transactions</span>
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
                placeholder="Search by account holder, number, or description..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field pl-10"
              />
            </div>
          </div>

          {/* Account Filter */}
          <div className="sm:w-48">
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <select
                value={accountFilter}
                onChange={(e) => setAccountFilter(e.target.value)}
                className="input-field pl-10 appearance-none"
              >
                <option value="all">All Accounts</option>
                {accounts.map((account) => (
                  <option key={account.acc_no} value={account.acc_no.toString()}>
                    Account #{account.acc_no}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Transaction Summary */}
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">
                {filteredTransactions.filter(t => t.type === 'deposit').length}
              </p>
              <p className="text-sm text-gray-600">Deposits</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-red-600">
                {filteredTransactions.filter(t => t.type === 'withdraw').length}
              </p>
              <p className="text-sm text-gray-600">Withdrawals</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-banking-600">
                ₹{filteredTransactions.reduce((sum, t) => 
                  sum + (t.type === 'deposit' ? t.amount : -t.amount), 0
                ).toLocaleString()}
              </p>
              <p className="text-sm text-gray-600">Net Amount</p>
            </div>
          </div>
        </div>
      </div>

      {/* Transactions List */}
      {filteredTransactions.length > 0 ? (
        <div className="card">
          <div className="card-header">
            <h2 className="text-lg font-semibold text-gray-900">Recent Transactions</h2>
          </div>
          
          <div className="space-y-4">
            {filteredTransactions.map((transaction) => {
              const IconComponent = getTransactionIcon(transaction.type);
              const colorClass = getTransactionColor(transaction.type);
              
              return (
                <div key={transaction.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className={`p-2 rounded-lg ${colorClass}`}>
                      <IconComponent className="h-5 w-5" />
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <p className="font-medium text-gray-900 capitalize">
                          {transaction.type}
                        </p>
                        <span className="text-gray-400">•</span>
                        <p className="text-sm text-gray-600">
                          Account #{transaction.account_no}
                        </p>
                      </div>
                      <p className="text-sm text-gray-600">{transaction.account_holder}</p>
                      <p className="text-xs text-gray-500">{transaction.description}</p>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <p className={`text-lg font-bold ${
                      transaction.type === 'deposit' ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {transaction.type === 'deposit' ? '+' : '-'}₹{transaction.amount.toLocaleString()}
                    </p>
                    <p className="text-sm text-gray-600">
                      Balance: ₹{transaction.balance_after.toLocaleString()}
                    </p>
                    <p className="text-xs text-gray-500">
                      {formatDate(transaction.date)}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <div className="card text-center py-12">
          <ArrowRightLeft className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No Transactions Found</h2>
          <p className="text-gray-600">
            {searchTerm || accountFilter !== 'all' 
              ? 'Try adjusting your search or filter criteria.' 
              : 'No transactions have been made yet.'
            }
          </p>
        </div>
      )}

      {/* Note about mock data */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start space-x-2">
          <Calendar className="h-5 w-5 text-blue-600 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-blue-800">Demo Data</p>
            <p className="text-sm text-blue-700">
              This page shows mock transaction data. In a real application, this would display 
              actual transaction history from your database.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Transactions;