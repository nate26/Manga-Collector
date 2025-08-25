export type AuthenticationData = {
  token: string;
  expiration: string;
  refresh_token: string;
};

export type UserData = {
  username: string;
  email: string;
  user_id: string;
  profile: {
    picture: string | null;
    banner: string | null;
    color: string | null;
    theme: string | null;
  };
  personal_stores: string[];
  authentication: AuthenticationData;
};

//TODO better way to do this in typescript without duplicating the type
export type AuthenticationDataPartial = {
  token: string | null;
  expiration: string | null;
  refresh_token: string | null;
};

export type UserDataPartial = {
  username: string | null;
  email: string | null;
  user_id: string | null;
  profile: {
    picture: string | null;
    banner: string | null;
    color: string | null;
    theme: string | null;
  };
  personal_stores: string[] | null;
  authentication: AuthenticationDataPartial;
};
