import { CommonModule } from '@angular/common';
import { Component, HostListener, inject, output, signal } from '@angular/core';
import { outputToObservable, takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { combineLatest, debounceTime, filter, map, startWith } from 'rxjs';
import { VolumeService } from '../../services/data/volume.service';

@Component({
  selector: 'app-search-volumes',
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './search-volumes.component.html',
  styleUrl: './search-volumes.component.css'
})
export class SearchVolumesComponent {
  private readonly _volumeService = inject(VolumeService);

  readonly selectVolume = output<any>();
  protected readonly disableSearchOnSelect = outputToObservable(this.selectVolume)
    .pipe(takeUntilDestroyed())
    .subscribe(() => this.searchActive.set(false));

  protected readonly searchActive = signal(true);

  protected readonly searchControl = new FormControl<string>('');
  protected readonly searchResults$ = combineLatest({
    volumes: this._volumeService.volumesBasic$,
    search: this.searchControl.valueChanges.pipe(startWith(''))
  }).pipe(
    debounceTime(300),
    filter(({ search }) => (search ?? '').length >= 3),
    map(({ volumes, search }) => {
      const filterValue = (search ?? '').toLowerCase();
      const filter = volumes
        .filter(vol => vol.display_name.toLowerCase().includes(filterValue))
        .map(vol => ({
          volume: vol,
          confidence: this.similarity(search ?? '', vol.display_name)
        }))
        .slice(0, 50);

      return filter
        .sort((a, b) => {
          const confidence = b.confidence - a.confidence;
          if (confidence) return confidence;
          else if (!a.volume.volume) return -1;
          else if (!b.volume.volume) return 1;
          else return a.volume.volume.localeCompare(b.volume.volume, undefined, { numeric: true });
        })
        .map(({ volume }) => volume);
    })
  );

  protected readonly similarity = (search: string, option: string) => {
    let longer = option;
    let shorter = search;
    if (option.length < search.length) {
      longer = search;
      shorter = option;
    }
    const longerLength = longer.length;
    if (longerLength == 0) {
      return 1.0;
    }
    return (longerLength - this.editDistance(longer, shorter)) / longerLength;
  };

  protected readonly editDistance = (s1: string, s2: string) => {
    s1 = s1.toLowerCase();
    s2 = s2.toLowerCase();

    const costs = [];
    for (let i = 0; i <= s1.length; i++) {
      let lastValue = i;
      for (let j = 0; j <= s2.length; j++) {
        if (i == 0) costs[j] = j;
        else {
          if (j > 0) {
            let newValue = costs[j - 1];
            if (s1.charAt(i - 1) != s2.charAt(j - 1))
              newValue = Math.min(Math.min(newValue, lastValue), costs[j]) + 1;
            costs[j - 1] = lastValue;
            lastValue = newValue;
          }
        }
      }
      if (i > 0) costs[s2.length] = lastValue;
    }
    return costs[s2.length];
  };

  @HostListener('document:keydown', ['$event'])
  protected hideOnEscape(event: KeyboardEvent) {
    if (event.key === 'Escape') this.searchActive.set(false);
  }
}
