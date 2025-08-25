import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { EMPTY, catchError, debounceTime, map, of, pipe, switchMap, throwError } from 'rxjs';
import { APIQueryService, Query } from './api-query.service';
import { UserService } from './user.service';
import { UserDataPartial } from './user.type';

export type Volume = {
  isbn: string;
  name: string;
  display_name: string;
  category: string;
  volume: string;
  brand: string;
  series: {
    title: string;
    url: string;
  };
  series_id: string;
  edition: string;
  edition_id: string;
  release_date: string;
  primary_cover_image: string;
};

type CollectionBase = {
  collection_id: string;
  collection: string;
  cost: number;
  store: string;
  purchase_date: string;
  read: boolean;
  tags: string[];
  user_id: string;
};

export type CollectionInput = CollectionBase & {
  isbn: string;
  user_id: string;
};

export type CollectionOutput = CollectionBase & {
  volume: Volume;
};

export type CollectionQuery = Query & {
  collection?: string;
  name?: string;
  category?: string;
  volume?: string;
  store?: string;
  read?: boolean;
  cost_le?: number;
  cost_ge?: number;
  purchase_date_le?: string;
  purchase_date_ge?: string;
  tags?: string[];
};

@Injectable({
  providedIn: 'root'
})
export class CollectionDataService {
  private readonly _http = inject(HttpClient);
  private readonly _queryService = inject(APIQueryService);
  private readonly _userService = inject(UserService);

  private readonly COLLECTION_PATH = 'http://localhost:4000/api/collection';

  private _checkUserId = pipe(
    map(({ user_id }: UserDataPartial) => {
      if (!user_id) {
        throw new Error('User data is missing');
      }
      return user_id;
    })
  );

  collectionSearch = pipe(
    map(
      (query: CollectionQuery) => this.COLLECTION_PATH + '?' + this._queryService.parseQuery(query)
    ),
    debounceTime(300),
    switchMap(url => this._http.get<CollectionOutput[]>(url)),
    catchError((err: Error) => {
      console.error('Could not get collection volume data because ', err);
      return EMPTY;
    })
  );

  getCollectionVolumes(query: CollectionQuery) {
    const url = this.COLLECTION_PATH + '?' + this._queryService.parseQuery(query);
    return of(url).pipe(
      debounceTime(300),
      switchMap(url => this._http.get<CollectionOutput[]>(url)),
      catchError((err: Error) => {
        console.error('Could not get collection volume data because ', err);
        return EMPTY;
      })
    );
  }

  createCollection(isbn: string) {
    return of(this._userService.userData()).pipe(
      this._checkUserId,
      map(user_id => this._buildNewRecord(isbn, user_id)),
      switchMap(collection =>
        this._http.post<CollectionOutput>(this.COLLECTION_PATH, {
          collection
        })
      ),
      catchError((err: Error) =>
        throwError(() => 'Could not create collection because ' + err.message)
      )
    );
  }

  updateCollection(collection_id: string, collectionInput: Partial<CollectionInput>) {
    return of(this._userService.userData()).pipe(
      this._checkUserId,
      map(user_id => ({ ...collectionInput, user_id }) as CollectionInput),
      switchMap(collection =>
        this._http.patch<CollectionOutput>(this.COLLECTION_PATH + '/' + collection_id, {
          collection
        })
      ),
      catchError((err: Error) =>
        throwError(() => 'Could not update collection because ' + err.message)
      )
    );
  }

  deleteCollection(collectionId: string) {
    return of(this._userService.userData()).pipe(
      this._checkUserId,
      switchMap(() =>
        this._http.delete<CollectionOutput>(this.COLLECTION_PATH + '/' + collectionId)
      ),
      catchError((err: Error) =>
        throwError(() => 'Could not delete collection because ' + err.message)
      )
    );
  }

  private _buildNewRecord(isbn: string, user_id: string): Partial<CollectionInput> {
    return {
      isbn,
      collection: 'Collection',
      read: false,
      tags: [],
      user_id,
      collection_id: window.crypto.randomUUID().toString()
    };
  }
}
