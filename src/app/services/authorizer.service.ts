import { EventEmitter, Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthorizerService {

  userIDs = ['f69c759a-00dd-4dbe-8e58-96cd7a05969e'];

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
