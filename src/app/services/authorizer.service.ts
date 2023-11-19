import { EventEmitter, Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthorizerService {

  userIDs = [''];

  activeUser: string | null = null;
  isAuthorized = false;

  authorizedEvent: EventEmitter<string> = new EventEmitter<string>();

  constructor() { }

  isUserAuthorized(): boolean {
    return this.isAuthorized;
  }

  authenticate(userID: string | null) {
    if (userID && this.userIDs.indexOf(userID) >= 0) {
      this.activeUser = userID;
      this.isAuthorized = true;
    }
  }
}
