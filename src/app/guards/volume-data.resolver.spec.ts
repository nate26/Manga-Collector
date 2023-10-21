import { TestBed } from '@angular/core/testing';

import { VolumeDataResolver } from './volume-data.resolver';

describe('VolumeDataResolver', () => {
  let resolver: VolumeDataResolver;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    resolver = TestBed.inject(VolumeDataResolver);
  });

  it('should be created', () => {
    expect(resolver).toBeTruthy();
  });
});
