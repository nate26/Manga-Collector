import { AsyncPipe } from '@angular/common';
import { Component, inject, Injector, input } from '@angular/core';
import { toObservable } from '@angular/core/rxjs-interop';
import {
  ControlValueAccessor,
  FormControl,
  NG_VALUE_ACCESSOR,
  ReactiveFormsModule
} from '@angular/forms';
import { combineLatest, debounceTime, map, Observable, shareReplay, startWith, tap } from 'rxjs';

@Component({
  selector: 'app-autofill-select-filter',
  imports: [AsyncPipe, ReactiveFormsModule],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      multi: true,
      useExisting: AutofillSelectFilterComponent
    }
  ],
  templateUrl: './autofill-select-filter.component.html',
  styleUrl: './autofill-select-filter.component.css'
})
export class AutofillSelectFilterComponent implements ControlValueAccessor {
  title = input.required<string>();
  list = input.required<string[]>();

  private readonly _injector = inject(Injector);

  list$ = toObservable(this.list).pipe(shareReplay(1));
  control = new FormControl('');
  filteredList!: Observable<string[]>;

  onTouch = () => {};

  writeValue(obj: string | undefined): void {
    this.control.setValue(obj ?? '', { emitEvent: false });
  }

  registerOnChange(fn: (_: string) => void): void {
    this.filteredList = combineLatest({
      value: this.control.valueChanges.pipe(startWith('')),
      options: toObservable(this.list, { injector: this._injector })
    }).pipe(
      debounceTime(1000),
      map(({ value, options }) => this._filter(value || '', options)),
      tap(() => fn(this.control.value ?? ''))
    );
  }

  registerOnTouched(fn: () => void): void {
    this.onTouch = fn;
  }

  setDisabledState?(isDisabled: boolean): void {
    if (isDisabled) {
      this.control.disable();
    } else {
      this.control.enable();
    }
  }

  private _filter(value: string, options: string[]): string[] {
    const filterValue = this._normalizeValue(value);
    return options.filter(option => this._normalizeValue(option).includes(filterValue));
  }

  private _normalizeValue(value: string): string {
    return value.toLowerCase().replace(/\s/g, '');
  }
}
