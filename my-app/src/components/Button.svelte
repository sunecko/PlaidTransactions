<script lang="ts">
  import { onMount } from 'svelte';
  import { getLinkToken, saveAccessToken} from '../store/api';
  import { goto } from '$app/navigation';

  let linkToken: string = '';

  async function loadPlaidScript() {
    return new Promise((resolve, reject) => {
      if (document.getElementById('plaid-script')) {
        resolve(null);
        return;
      }

      const script = document.createElement('script');
      script.id = 'plaid-script';
      script.src = 'https://cdn.plaid.com/link/v2/stable/link-initialize.js';
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  async function initializePlaidLink() {
    try {
      const tokenResponse = await getLinkToken();
      linkToken = tokenResponse;

      const handler = (window as any).Plaid.create({
        token: linkToken,
        onSuccess: (public_token: string, metadata: any) => {
          console.log('Public token:', public_token);
          saveAccessToken(public_token);
          goto('/transactions');
        },
        onExit: (error: any, metadata: any) => {
          if (error) {
            console.error('Error', error);
          }
        },
        onEvent: (eventName: any, metadata: any) => {
          console.log('Event', eventName, metadata);
        }
      });

      document.getElementById('openLink')?.addEventListener('click', () => {
        handler.open();
      });

    } catch (error) {
      console.error('Error fetching link token or initializing Plaid Link', error);
    }
  }

  onMount(async () => {
    try {
      await loadPlaidScript();
      await initializePlaidLink();
    } catch (error) {
      console.error('Error loading Plaid script or initializing Plaid Link', error);
    }
  });
</script>

<button id="openLink">Click Here</button>

<style>
#openLink {
    background-color: #c35510; 
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 12px;
    transition-duration: 0.4s;
}

#openLink:hover {
    background-color: white;
    color: black;
    border: 2px solid #c35510;
}
</style>
