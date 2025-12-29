import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { 
  X, 
  DollarSign, 
  TrendingUp, 
  TrendingDown, 
  AlertCircle,
  CreditCard
} from 'lucide-react';
import { useBank } from '../../context/BankContext';

const TransactionModal = ({ 
  isOpen, 
  onClose, 
  accountId, 
  accountBalance, 
  accountHolder, 
  transactionType = 'deposit' // 'deposit' or 'withdraw'
}) => {
  const { deposit, withdraw, loading } = useBank();
  const [isProcessing, setIsProcessing] = useState(false);
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch
  } = useForm();

  const amount = watch('amount');

  const onSubmit = async (data) => {
    setIsProcessing(true);
    
    const transactionAmount = parseFloat(data.amount);
    let result;

    if (transactionType === 'deposit') {
      result = await deposit(accountId, transactionAmount);
    } else {
      result = await withdraw(accountId, transactionAmount);
    }

    if (result.success) {
      reset();
      onClose();
    }
    
    setIsProcessing(false);
  };

  const handleClose = () => {
    reset();
    onClose();
  };

  if (!isOpen) return null;

  const isDeposit = transactionType === 'deposit';
  const icon = isDeposit ? TrendingUp : TrendingDown;
  const IconComponent = icon;
  const title = isDeposit ? 'Deposit Money' : 'Withdraw Money';
  const buttonText = isDeposit ? 'Deposit' : 'Withdraw';
  const colorClass = isDeposit ? 'text-green-600' : 'text-red-600';
  const bgColorClass = isDeposit ? 'bg-green-100' : 'bg-red-100';
  const buttonColorClass = isDeposit ? 'btn-primary' : 'btn-danger';

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl shadow-xl max-w-md w-full">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div className="flex items-center space-x-3">
            <div className={`p-2 ${bgColorClass} rounded-lg`}>
              <IconComponent className={`h-6 w-6 ${colorClass}`} />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
              <p className="text-sm text-gray-600">Account #{accountId}</p>
            </div>
          </div>
          <button
            onClick={handleClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>

        {/* Account Info */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-900">{accountHolder}</p>
              <p className="text-sm text-gray-600">Current Balance</p>
            </div>
            <div className="text-right">
              <p className="text-lg font-bold text-banking-600">
                ₹{accountBalance?.toLocaleString()}
              </p>
            </div>
          </div>
        </div>

        {/* Transaction Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-6">
          {/* Amount Input */}
          <div>
            <label htmlFor="amount" className="block text-sm font-medium text-gray-700 mb-2">
              Amount (₹)
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <DollarSign className="h-5 w-5 text-gray-400" />
              </div>
              <input
                {...register('amount', {
                  required: 'Amount is required',
                  min: {
                    value: 1,
                    message: 'Amount must be at least ₹1',
                  },
                  max: !isDeposit ? {
                    value: accountBalance,
                    message: `Amount cannot exceed current balance (₹${accountBalance?.toLocaleString()})`,
                  } : undefined,
                  validate: (value) => {
                    const num = parseFloat(value);
                    if (isNaN(num)) return 'Please enter a valid number';
                    if (num <= 0) return 'Amount must be greater than 0';
                    if (!isDeposit && num > accountBalance) {
                      return 'Insufficient balance';
                    }
                    return true;
                  },
                })}
                type="number"
                step="0.01"
                min="1"
                max={!isDeposit ? accountBalance : undefined}
                className="input-field pl-10"
                placeholder="Enter amount"
              />
            </div>
            {errors.amount && (
              <p className="mt-1 text-sm text-red-600">{errors.amount.message}</p>
            )}
          </div>

          {/* Transaction Preview */}
          {amount && !errors.amount && (
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-gray-900 mb-2">Transaction Preview</h4>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Current Balance:</span>
                  <span className="font-medium">₹{accountBalance?.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">{isDeposit ? 'Deposit' : 'Withdraw'} Amount:</span>
                  <span className={`font-medium ${colorClass}`}>
                    {isDeposit ? '+' : '-'}₹{parseFloat(amount || 0).toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between border-t border-gray-200 pt-2">
                  <span className="font-medium text-gray-900">New Balance:</span>
                  <span className="font-bold text-banking-600">
                    ₹{(accountBalance + (isDeposit ? parseFloat(amount || 0) : -parseFloat(amount || 0))).toLocaleString()}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Warning for large withdrawals */}
          {!isDeposit && amount && parseFloat(amount) > accountBalance * 0.5 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 flex items-start space-x-2">
              <AlertCircle className="h-5 w-5 text-yellow-600 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-yellow-800">Large Withdrawal</p>
                <p className="text-sm text-yellow-700">
                  You're withdrawing more than 50% of your balance. Please ensure this is intended.
                </p>
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <button
              type="button"
              onClick={handleClose}
              className="flex-1 btn-secondary"
              disabled={isProcessing || loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className={`flex-1 ${buttonColorClass} disabled:opacity-50 disabled:cursor-not-allowed`}
              disabled={isProcessing || loading || !amount || parseFloat(amount) <= 0}
            >
              {isProcessing || loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Processing...
                </div>
              ) : (
                <>
                  <IconComponent className="h-4 w-4 mr-2" />
                  {buttonText} ₹{parseFloat(amount || 0).toLocaleString()}
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TransactionModal;