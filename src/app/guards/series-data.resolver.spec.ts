import { TestBed } from '@angular/core/testing';

import { SeriesDataResolver } from './series-data.resolver';

describe('SeriesDataResolver', () => {
  let resolver: SeriesDataResolver;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    resolver = TestBed.inject(SeriesDataResolver);
  });

  it('should be created', () => {
    expect(resolver).toBeTruthy();
  });
});
