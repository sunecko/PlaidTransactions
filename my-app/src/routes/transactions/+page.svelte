<script lang="ts">
  import TransactionTable from '../../components/TransactionsTable.svelte';
  
  let loading = false;
  const error: string | null = null;
</script>

<h1>Transacciones</h1>
{#if loading}
  <p>Cargando...</p>
{:else}
  <TransactionTable />
{/if}
