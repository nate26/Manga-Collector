import { Routes } from '@angular/router';

import { loggedInGuard } from './guards/logged-in.guard';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/volumes',
    pathMatch: 'full'
  },
  {
    path: 'volumes',
    loadComponent: () =>
      import('../pages/volumes/(browse-volumes).page').then(m => m.BrowseVolumesPage)
  },
  {
    path: 'series',
    loadComponent: () =>
      import('../pages/series/(browse-series).page').then(m => m.BrowseSeriesPage)
  },
  {
    path: 'series/:series_id',
    loadComponent: () => import('../pages/series/[seriesId].page').then(m => m.SeriesIdPage)
  },
  {
    path: 'collection/volumes',
    loadComponent: () =>
      import('../pages/collection/volumes/(collection-volumes).page').then(
        m => m.CollectionVolumesPage
      ),
    canActivate: [loggedInGuard]
  },
  {
    path: '**',
    loadComponent: () => import('../pages/[...not-found].page').then(m => m.NotFoundPage)
  }
];
