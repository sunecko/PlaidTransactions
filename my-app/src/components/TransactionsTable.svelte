<script lang="ts">
  import { onMount } from 'svelte';
  import axios from 'axios';
  
    let transactionsData: any[] = [];

        const fetchTransactions = async() =>  {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/get-transactions/');
            transactionsData = response.data.transactions;
            console.log(transactionsData)
        } catch (err) {
            const error = 'Failed to fet  ch transactions';
            console.error(err);
        } 
    }
    onMount(fetchTransactions); 
  </script>
  
  <div class="transactions-wrapper">
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Amount</th>
            <th>Category</th>
            <th>Merchant</th>
            <th>Currency</th>
            <th>Payment Channel</th>
          </tr>
        </thead>
        <tbody>
          {#each transactionsData as transaction}
            <tr>
              <td>{transaction.date}</td>
              <td>${transaction.amount.toFixed(2)}</td>
              <td>{transaction.category}</td>
              <td>{transaction.merchant_name}</td>
              <td>{transaction.iso_currency_code}</td>
              <td>{transaction.payment_channel}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>


  <style>
    .transactions-wrapper {
      min-width: 1000px;
      max-width: 1200px; 
      margin: 0 auto; 
      overflow-x: auto; 
    }
  
    .table-wrapper {
      overflow-x: auto;
    }
  
    table {
      width: 100%;
      border-collapse: collapse;
    }
  
    th, td {
      border: 1px solid #ddd;
      padding: 8px;
      text-align: left;
    }
  
    th {
      background-color: #f2f2f2;
    }
  </style>
