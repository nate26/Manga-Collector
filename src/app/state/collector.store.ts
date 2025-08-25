import { signalStore, withState } from '@ngrx/signals';
import { ShopQuery } from '../services/data/sale-data.service';

// TODO add more
type MCPath = 'home' | 'volumes' | 'series' | 'collection/volumes' | 'collection/series';

type NavigationState = {
  filter: ShopQuery;
  path: MCPath;
};

const initialState: NavigationState = {
  filter: {},
  path: 'home'
};

export const CollectorStore = signalStore(withState(initialState));
