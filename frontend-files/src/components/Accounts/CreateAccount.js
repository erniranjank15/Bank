import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { 
  ArrowLeft, 
  CreditCard, 
  User, 
  MapPin, 
  Calendar,
  Building2,
  Hash,
  DollarSign
} from 'lucide-react';
import { useBank } from '../../context/BankContext';

const CreateAccount = () => {
  const navigate = useNavigate();
  const { createAccount, loading } = useBank();
  
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const onSubmit = async (data) => {
    const accountData = {
      acc_holder_name: data.acc_holder_name,
      acc_holder_address: data.acc_holder_address,
      dob: data.dob,
      gender: data.gender,
      acc_type: data.acc_type,
      balance: parseFloat(data.balance),
      ifsc_code: parseInt(data.ifsc_code),
      branch: data.branch,
    };

    const result = await createAccount(accountData);
    if (result.success) {
      navigate('/accounts');
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <button
          onClick={() => navigate('/accounts')}
          className="p-2 hover:bg-gray-100 rounded-full transition-colors"
        >
          <ArrowLeft className="h-5 w-5 text-gray-600" />
        </button>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Create New Account</h1>
          <p className="text-gray-600">Open a new bank account</p>
        </div>
      </div>

      {/* Form */}
      <div className="card max-w-2xl">
        <div className="card-header">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-banking-100 rounded-lg">
              <CreditCard className="h-6 w-6 text-banking-600" />
            </div>
            <h2 className="text-xl font-semibold text-gray-900">Account Information</h2>
          </div>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Personal Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Account Holder Name */}
            <div>
              <label htmlFor="acc_holder_name" className="block text-sm font-medium text-gray-700 mb-2">
                Account Holder Name
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  {...register('acc_holder_name', {
                    required: 'Account holder name is required',
                    minLength: {
                      value: 2,
                      message: 'Name must be at least 2 characters',
                    },
                  })}
                  type="text"
                  className="input-field pl-10"
                  placeholder="Enter full name"
                />
              </div>
              {errors.acc_holder_name && (
                <p className="mt-1 text-sm text-red-600">{errors.acc_holder_name.message}</p>
              )}
            </div>

            {/* Date of Birth */}
            <div>
              <label htmlFor="dob" className="block text-sm font-medium text-gray-700 mb-2">
                Date of Birth
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Calendar className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  {...register('dob', {
                    required: 'Date of birth is required',
                  })}
                  type="date"
                  className="input-field pl-10"
                />
              </div>
              {errors.dob && (
                <p className="mt-1 text-sm text-red-600">{errors.dob.message}</p>
              )}
            </div>
          </div>

          {/* Address */}
          <div>
            <label htmlFor="acc_holder_address" className="block text-sm font-medium text-gray-700 mb-2">
              Address
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MapPin className="h-5 w-5 text-gray-400" />
              </div>
              <textarea
                {...register('acc_holder_address', {
                  required: 'Address is required',
                  minLength: {
                    value: 10,
                    message: 'Address must be at least 10 characters',
                  },
                })}
                rows={3}
                className="input-field pl-10"
                placeholder="Enter complete address"
              />
            </div>
            {errors.acc_holder_address && (
              <p className="mt-1 text-sm text-red-600">{errors.acc_holder_address.message}</p>
            )}
          </div>

          {/* Gender and Account Type */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Gender */}
            <div>
              <label htmlFor="gender" className="block text-sm font-medium text-gray-700 mb-2">
                Gender
              </label>
              <select
                {...register('gender', {
                  required: 'Gender is required',
                })}
                className="input-field"
              >
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
              {errors.gender && (
                <p className="mt-1 text-sm text-red-600">{errors.gender.message}</p>
              )}
            </div>

            {/* Account Type */}
            <div>
              <label htmlFor="acc_type" className="block text-sm font-medium text-gray-700 mb-2">
                Account Type
              </label>
              <select
                {...register('acc_type', {
                  required: 'Account type is required',
                })}
                className="input-field"
              >
                <option value="">Select Account Type</option>
                <option value="Savings">Savings Account</option>
                <option value="Current">Current Account</option>
                <option value="Fixed">Fixed Deposit</option>
              </select>
              {errors.acc_type && (
                <p className="mt-1 text-sm text-red-600">{errors.acc_type.message}</p>
              )}
            </div>
          </div>

          {/* Bank Details */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Initial Balance */}
            <div>
              <label htmlFor="balance" className="block text-sm font-medium text-gray-700 mb-2">
                Initial Balance (₹)
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <DollarSign className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  {...register('balance', {
                    required: 'Initial balance is required',
                    min: {
                      value: 100,
                      message: 'Minimum balance is ₹100',
                    },
                  })}
                  type="number"
                  step="0.01"
                  min="100"
                  className="input-field pl-10"
                  placeholder="Minimum ₹100"
                  defaultValue="100"
                />
              </div>
              {errors.balance && (
                <p className="mt-1 text-sm text-red-600">{errors.balance.message}</p>
              )}
            </div>

            {/* IFSC Code */}
            <div>
              <label htmlFor="ifsc_code" className="block text-sm font-medium text-gray-700 mb-2">
                IFSC Code
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Hash className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  {...register('ifsc_code', {
                    required: 'IFSC code is required',
                  })}
                  type="number"
                  className="input-field pl-10"
                  placeholder="123456"
                  defaultValue="123456"
                />
              </div>
              {errors.ifsc_code && (
                <p className="mt-1 text-sm text-red-600">{errors.ifsc_code.message}</p>
              )}
            </div>
          </div>

          {/* Branch */}
          <div>
            <label htmlFor="branch" className="block text-sm font-medium text-gray-700 mb-2">
              Branch
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Building2 className="h-5 w-5 text-gray-400" />
              </div>
              <input
                {...register('branch', {
                  required: 'Branch is required',
                })}
                type="text"
                className="input-field pl-10"
                placeholder="Main Branch"
                defaultValue="Main Branch"
              />
            </div>
            {errors.branch && (
              <p className="mt-1 text-sm text-red-600">{errors.branch.message}</p>
            )}
          </div>

          {/* Submit Buttons */}
          <div className="flex space-x-4 pt-6 border-t border-gray-200">
            <button
              type="button"
              onClick={() => navigate('/accounts')}
              className="flex-1 btn-secondary"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-1 btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Creating Account...
                </div>
              ) : (
                <>
                  <CreditCard className="h-5 w-5 mr-2" />
                  Create Account
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateAccount;