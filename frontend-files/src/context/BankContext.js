import React, { createContext, useContext, useReducer } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

// Initial state
const initialState = {
  users: [],
  accounts: [],
  currentAccount: null,
  loading: false,
  error: null,
};

// Action types
const BANK_ACTIONS = {
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR',
  SET_USERS: 'SET_USERS',
  SET_ACCOUNTS: 'SET_ACCOUNTS',
  SET_CURRENT_ACCOUNT: 'SET_CURRENT_ACCOUNT',
  ADD_USER: 'ADD_USER',
  ADD_ACCOUNT: 'ADD_ACCOUNT',
  UPDATE_ACCOUNT: 'UPDATE_ACCOUNT',
  DELETE_ACCOUNT: 'DELETE_ACCOUNT',
};

// Reducer
const bankReducer = (state, action) => {
  switch (action.type) {
    case BANK_ACTIONS.SET_LOADING:
      return { ...state, loading: action.payload };
    case BANK_ACTIONS.SET_ERROR:
      return { ...state, error: action.payload, loading: false };
    case BANK_ACTIONS.CLEAR_ERROR:
      return { ...state, error: null };
    case BANK_ACTIONS.SET_USERS:
      return { ...state, users: action.payload, loading: false };
    case BANK_ACTIONS.SET_ACCOUNTS:
      return { ...state, accounts: action.payload, loading: false };
    case BANK_ACTIONS.SET_CURRENT_ACCOUNT:
      return { ...state, currentAccount: action.payload, loading: false };
    case BANK_ACTIONS.ADD_USER:
      return { ...state, users: [...state.users, action.payload], loading: false };
    case BANK_ACTIONS.ADD_ACCOUNT:
      return { ...state, accounts: [...state.accounts, action.payload], loading: false };
    case BANK_ACTIONS.UPDATE_ACCOUNT:
      return {
        ...state,
        accounts: state.accounts.map(acc => 
          acc.acc_no === action.payload.acc_no ? action.payload : acc
        ),
        currentAccount: state.currentAccount?.acc_no === action.payload.acc_no 
          ? action.payload 
          : state.currentAccount,
        loading: false,
      };
    case BANK_ACTIONS.DELETE_ACCOUNT:
      return {
        ...state,
        accounts: state.accounts.filter(acc => acc.acc_no !== action.payload),
        currentAccount: state.currentAccount?.acc_no === action.payload 
          ? null 
          : state.currentAccount,
        loading: false,
      };
    default:
      return state;
  }
};

// Create context
const BankContext = createContext();

// Bank Provider
export const BankProvider = ({ children }) => {
  const [state, dispatch] = useReducer(bankReducer, initialState);

  // Helper function to handle API errors
  const handleError = (error, defaultMessage = 'An error occurred') => {
    const errorMessage = error.response?.data?.detail || defaultMessage;
    dispatch({ type: BANK_ACTIONS.SET_ERROR, payload: errorMessage });
    toast.error(errorMessage);
    return errorMessage;
  };

  // User operations
  const createUser = async (userData) => {
    try {
      dispatch({ type: BANK_ACTIONS.SET_LOADING, payload: true });
      const response = await axios.post('/users/', userData);
      dispatch({ type: BANK_ACTIONS.ADD_USER, payload: response.data });
      toast.success('User created successfully!');
      return { success: true, data: response.data };
    } catch (error) {
      handleError(error, 'Failed to create user');
      return { success: false };
    }
  };

  const fetchUsers = async () => {
    try {
      dispatch({ type: BANK_ACTIONS.SET_LOADING, payload: true });
      const response = await axios.get('/users/');
      dispatch({ type: BANK_ACTIONS.SET_USERS, payload: response.data });
      return { success: true, data: response.data };
    } catch (error) {
      handleError(error, 'Failed to fetch users');
      return { success: false };
    }
  };

  const fetchUserProfile = async (userId) => {
    try {
      dispatch({ type: BANK_ACTIONS.SET_LOADING, payload: true });
      const response = await axios.get(`/users/${userId}`);
      return { success: true, data: response.data };
    } catch (error) {
      handleError(error, 'Failed to fetch user profile');
      return { success: false };
    }
  };

  // Account operations
  const createAccount = async (accountData) => {
    try {
      dispatch({ type: BANK_ACTIONS.SET_LOADING, payload: true });
      const response = await axios.post('/accounts/', accountData);
      dispatch({ type: BANK_ACTIONS.ADD_ACCOUNT, payload: response.data });
      toast.success('Account created successfully!');
      return { success: true, data: response.data };
    } catch (error) {
      handleError(error, 'Failed to create account');
      return { success: false };
    }
  };

  const fetchAccounts = async () => {
    try {
      dispatch({ type: BANK_ACTIONS.SET_LOADING, payload: true });
      const response = await axios.get('/accounts/');
      dispatch({ type: BANK_ACTIONS.SET_ACCOUNTS, payload: response.data });
      return { success: true, data: response.data };
    } catch (error) {
      handleError(error, 'Failed to fetch accounts');
      return { success: false };
    }
  };

  const fetchAccount = async (accountId) => {
    try {
      dispatch({ type: BANK_ACTIONS.SET_LOADING, payload: true });
      const response = await axios.get(`/accounts/${accountId}`);
      dispatch({ type: BANK_ACTIONS.SET_CURRENT_ACCOUNT, payload: response.data });
      return { success: true, data: response.data };
    } catch (error) {
      handleError(error, 'Failed to fetch account');
      return { success: false };
    }
  };

  const updateAccount = async (accountId, updateData) => {
    try {
      dispatch({ type: BANK_ACTIONS.SET_LOADING, payload: true });
      const response = await axios.patch(`/accounts/${accountId}`, updateData);
      dispatch({ type: BANK_ACTIONS.UPDATE_ACCOUNT, payload: response.data });
      toast.success('Account updated successfully!');
      return { success: true, data: response.data };
    } catch (error) {
      handleError(error, 'Failed to update account');
      return { success: false };
    }
  };

  const deleteAccount = async (accountId) => {
    try {
      dispatch({ type: BANK_ACTIONS.SET_LOADING, payload: true });
      await axios.delete(`/accounts/${accountId}`);
      dispatch({ type: BANK_ACTIONS.DELETE_ACCOUNT, payload: accountId });
      toast.success('Account deleted successfully!');
      return { success: true };
    } catch (error) {
      handleError(error, 'Failed to delete account');
      return { success: false };
    }
  };

  // Transaction operations
  const deposit = async (accountId, amount) => {
    try {
      dispatch({ type: BANK_ACTIONS.SET_LOADING, payload: true });
      const response = await axios.post(`/accounts/${accountId}/deposit?amount=${amount}`);
      dispatch({ type: BANK_ACTIONS.UPDATE_ACCOUNT, payload: response.data });
      toast.success(`Successfully deposited $${amount}`);
      return { success: true, data: response.data };
    } catch (error) {
      handleError(error, 'Failed to deposit');
      return { success: false };
    }
  };

  const withdraw = async (accountId, amount) => {
    try {
      dispatch({ type: BANK_ACTIONS.SET_LOADING, payload: true });
      const response = await axios.post(`/accounts/${accountId}/withdraw?amount=${amount}`);
      dispatch({ type: BANK_ACTIONS.UPDATE_ACCOUNT, payload: response.data });
      toast.success(`Successfully withdrew $${amount}`);
      return { success: true, data: response.data };
    } catch (error) {
      handleError(error, 'Failed to withdraw');
      return { success: false };
    }
  };

  // Clear error
  const clearError = () => {
    dispatch({ type: BANK_ACTIONS.CLEAR_ERROR });
  };

  const value = {
    ...state,
    createUser,
    fetchUsers,
    fetchUserProfile,
    createAccount,
    fetchAccounts,
    fetchAccount,
    updateAccount,
    deleteAccount,
    deposit,
    withdraw,
    clearError,
  };

  return (
    <BankContext.Provider value={value}>
      {children}
    </BankContext.Provider>
  );
};

// Custom hook to use bank context
export const useBank = () => {
  const context = useContext(BankContext);
  if (!context) {
    throw new Error('useBank must be used within a BankProvider');
  }
  return context;
};