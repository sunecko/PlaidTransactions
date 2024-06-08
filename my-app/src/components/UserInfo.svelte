<script>
  // Datos de ejemplo del usuario
  export let userInfo = {
      name: "Nombre de Usuario",
      accountName: "Plaid Checking",
      balance: 110.00,
      profilePic: "pic_url"
  };
</script>

<div class="user-info">
  <div class="profile-pic"></div>
  <h2>{userInfo.name}</h2>
  <p>Nombre de la cuenta: {userInfo.accountName}</p>
  <p>Saldo actual: ${userInfo.balance}</p>
</div>


<style>
  /* Estilos CSS */
  .user-info {
    position: absolute;
    top: 20px;
    right: 20px;
    text-align: center;
  }

  .profile-pic {
    width: 100px;
    height: 100px;
    background-color: #ccc;
    border-radius: 50%; 
    margin: 0 auto 10px; 
    background-image: url({userInfo.profilePic}); 
    background-size: cover; 
  }

  .user-info h2 {
    font-size: 24px;
    margin-bottom: 5px;
  }

  .user-info p {
    font-size: 16px;
    margin-bottom: 5px;
  }
</style>
