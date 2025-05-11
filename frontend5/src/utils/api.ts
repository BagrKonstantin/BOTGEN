import { API_BASE_URL, endpoints } from '../config/api';
import { useAuthStore } from '../store/authStore';

export async function fetchWithAuth(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  const store = useAuthStore.getState();
  const headers = {
    ...options.headers,
    Authorization: `${store.tokenType} ${store.accessToken}`,
  };

  let response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    store.clearAuth();
  }

  // if (response.status === 401) {
  //   const errorJSON = await response.json();
  //   console.log(errorJSON);
  //   if (errorJSON.detail.includes('Invalid token')) {
  //     store.clearAuth();
  //   }
  //   if (errorJSON.detail.includes('Token has expired')) {
  //     try {
  //       const refreshResponse = await fetch(
  //         `${API_BASE_URL}${endpoints.refreshToken}`,
  //         {
  //           headers: {
  //             Authorization: `${store.tokenType} ${store.accessToken}`,
  //           },
  //         }
  //       );
  //
  //       if (refreshResponse.ok) {
  //         const { access_token, token_type } = await refreshResponse.json();
  //         store.setAccessToken(access_token, token_type);
  //
  //         // Retry the original request with the new token
  //         response = await fetch(`${API_BASE_URL}${endpoint}`, {
  //           ...options,
  //           headers: {
  //             ...options.headers,
  //             Authorization: `${token_type} ${access_token}`,
  //           },
  //         });
  //       } else {
  //         store.clearAuth();
  //         throw new Error('Token refresh failed');
  //       }
  //     } catch (error) {
  //       store.clearAuth();
  //       throw error;
  //     }
  //   }
  // }

  try {
    const refreshResponse = await fetch(
        `${API_BASE_URL}${endpoints.refreshToken}`,
        {
          headers: {
            Authorization: `${store.tokenType} ${store.accessToken}`,
          },
        }
    );

    if (refreshResponse.ok) {
      const { access_token, token_type } = await refreshResponse.json();
      store.setAccessToken(access_token, token_type);

    } else {
      store.clearAuth();
      throw new Error('Token refresh failed');
    }
  } catch (error) {
    store.clearAuth();
    throw error;
  }

  return response;
}