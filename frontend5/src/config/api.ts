const api_host = "185.128.107.147"

export const API_BASE_URL = `http://${api_host}:8000`;

export const endpoints = {
  login: (username: string) => `/login/${username}`,
  checkLoginStatus: (token: string) => `/is-login-approved/${token}`,
  refreshToken: '/refresh_token',
  allBots: '/all-bots',
  newBot: (botToken: string) => `/new-bot/${botToken}`,
  deleteBot: (botId: number) => `/delete-bot/${botId}`,
  launchBot: (botId: number) => `/launch-bot/${botId}`,
  stopBot: (botId: number) => `/stop-bot/${botId}`,
  getBot: (botId: number) => `/get-bot/${botId}`,
  uploadImage: (botId: number) => `/upload-image/${botId}`,
  getImage: (botId: number, imageId: string) => `/get-image/${botId}/${imageId}`,
  saveBot: (botId: number) => `/save-bot/${botId}`,
  getAllProductTypes: (botId: number) => `/get-all-product-types/${botId}`,
  getAllProducts: (productTypeId: number) => `/get-all-products/${productTypeId}`,
  uploadProduct: (productTypeId: number) => `/upload-product/${productTypeId}`,
  deleteProduct: (productId: number) => `/delete-product/${productId}`,
  deleteProductType: (productTypeId: number) => `/delete-product-type/${productTypeId}`,
  getBotSettings: (botId: number) => `/get-bot-settings/${botId}`,
  saveBotSettings: (botId: number) => `/save-settings/${botId}`,
};