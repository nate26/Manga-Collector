import { Routes } from '@angular/router';

import { loggedInGuard } from './guards/logged-in.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/sales',
    pathMatch: 'full'
  },
  {
    path: 'sales',
    loadComponent: () =>
      import('./page-components/browse-sales/browse-sales.component').then(
        m => m.BrowseSalesComponent
      )
  },
  {
    path: 'series',
    loadComponent: () =>
      import('./page-components/series/series.component').then(m => m.SeriesComponent),
    canActivate: [loggedInGuard]
  },
  {
    path: 'series/:series_id',
    loadComponent: () =>
      import('./page-components/series-details/series-details.component').then(
        m => m.SeriesDetailsComponent
      ),
    canActivate: [loggedInGuard]
  },
  {
    path: 'collection',
    loadComponent: () =>
      import('./page-components/collection/collection.component').then(m => m.CollectionComponent),
    canActivate: [loggedInGuard]
  },
  {
    path: '**',
    loadComponent: () =>
      import('./home/page-not-found/page-not-found.component').then(m => m.PageNotFoundComponent)
  }
];
