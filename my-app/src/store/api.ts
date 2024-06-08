import { writable } from 'svelte/store';
import axios from 'axios';
import type { Transaction } from '../types/transactions';

export let transactions = writable<Transaction[]>([]);

const getLinkToken = async () => {
  try {
    const response = await axios.post<{token_link:string}>('http://127.0.0.1:8000/api/token-create', {}, {
      headers : {
        'Content-Type': 'application/json'
      }
    });
    return response.data.token_link;
  } catch (error) {
    console.error("Error fetching link token", error);
    throw error; 
  }
};

const saveAccessToken = async (token: string) => {
  try {
    console.log(token)
    const response = await axios.post('http://127.0.0.1:8000/api/token/save', {
      token: token
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    console.log('Access token saved:', response.data);
  } catch (error) {
    console.error('Error saving access token', error);
  }
}

export {  getLinkToken, saveAccessToken };
