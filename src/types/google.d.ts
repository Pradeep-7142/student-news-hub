interface Window {
  google: {
    accounts: {
      id: {
        initialize: (config: {
          client_id: string;
          callback: (response: { credential: string }) => void;
        }) => void;
        prompt: (callback: (notification: { isNotDisplayed: () => boolean }) => void) => void;
      };
    };
  };
}