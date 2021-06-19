import React from 'react';
import style from './FiltersManager.module.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faTimes } from '@fortawesome/free-solid-svg-icons';
import { AppConsumer, AppContextProps, Response } from './AppContext';
import Popup from './Popup';
import FancyCollapse from './FancyCollapse';

interface FiltersManagerProps {
};

interface Filter {
  name: string;
  desc: string;
  props: {
    name: string;
    min: number;
    max: number;
    step: number;
    value?: number;
  }[];
};

interface ActiveFilter {
  name: string;
  [key: string]: any;
};

interface FiltersManagerState {
  filters: ActiveFilter[];
  allFilters: Filter[];
};

export default class FiltersManager extends React.Component<FiltersManagerProps, FiltersManagerState> {
  public context: AppContextProps;
  private selectFilterPopup: Popup;
  private lastChange: number[];

  constructor (props) {
    super(props);
    this.state = {
      filters: [],
      allFilters: [],
    };
  }

  public componentDidMount(): void {
    this.refresh();
  }

  public refresh (): void {
    this.refreshCurrent();
    this.refreshAvailable();
  }

  private refreshCurrent (): void {
    interface FiltersResponse extends Response {
      filters: ActiveFilter[];
    }
    this.context.req<FiltersResponse>('sh filters', {})
    .then(res => {
      console.log(res);
      this.setState({
        filters: !res.success ? [] : res.filters,
      }, () => this.lastChange = new Array(this.state.filters.length).fill(Date.now()));
    });
  }

  private refreshAvailable (): void {
    interface FiltersResponse extends Response {
      filters: Filter[];
    }
    this.context.req<FiltersResponse>('sh filters a', {})
    .then(res => {
      this.setState({
        allFilters: !res.success ? [] : res.filters,
      });
    });
  }

  private addFilter (name: string, ...args: any[]): void {
    this.context.req<Response>(`start filter ${name} ${args.join(' ')}`, {})
    .then(() => this.refreshCurrent());
  }

  private onAddFilter (): void {
    this.refreshAvailable();
    this.selectFilterPopup.show();
  }

  private getFilter (name: string): Filter {
    return this.state.allFilters.filter(f => f.name === name)[0];
  }

  private onSelectFilter (name: string): void {
    const filter: Filter = this.getFilter(name);
    if (!filter) return;
    this.addFilter(filter.name, ...filter.props.map(p => typeof p.value !== 'undefined' ? p.value : p.min));
  }

  private stopFilter (ind: number): void {
    this.context.req<Response>(`stop filter ${ind}`, {})
    .then(() => this.refreshCurrent());
  }

  private onStopFilter (e: React.MouseEvent, i: number): void {
    e.stopPropagation();
    this.stopFilter(i);
  }

  private updateFilter (ind: number, args: any[]): void {
    this.context.req<Response>(`set filter ${ind} ${args.join(' ')}`, {});
  }

  private onChangeParameter (e: React.ChangeEvent, i: number): void {
    if (Date.now() - this.lastChange[i] < 25) return;
    this.lastChange[i] = Date.now();
    const filters: ActiveFilter[] = this.state.filters;
    const values: any[] = [];
    Array.from(e.target.parentElement.parentElement.getElementsByTagName('input')).forEach(inp => {
      values.push(inp.value);
      filters[i][inp.name] = inp.value;
    });
    this.setState({
      filters,
    }, () => this.updateFilter(i, values));
  }

  public render (): React.ReactElement {
    return (
      <AppConsumer>
        {ctx => {
          this.context = ctx;
          return (
            <div className={style.root}>
              {
                this.state.filters.length > 0
                ? (<div className={style.currentFilters}>
                  {
                    this.state.filters.map((f: ActiveFilter, i: number) => 
                      <FancyCollapse key={i} title={f.name} 
                        titleElements={
                          <i className={style.closeFilter} onClick={e => this.onStopFilter(e, i)}>
                            <FontAwesomeIcon icon={faTimes} />
                          </i>
                        }
                      >
                      {
                        this.getFilter(f.name).props.length > 0
                        ? (<form className={style.filterForm}>{this.getFilter(f.name).props.map(p => 
                            <div key={p.name} className={style.formRow}>
                              <label>
                                {p.name}
                              </label>
                              <input 
                                type="range" 
                                name={p.name} 
                                min={p.min} 
                                max={p.max} 
                                step={p.step} 
                                value={this.state.filters[i][p.name]} 
                                onChange={e => this.onChangeParameter(e, i)}
                              />
                            </div>)}
                          </form>)
                        : ''
                      }
                      </FancyCollapse>)
                  }
                  </div>)
                : ''
              }
              <div className={style.add} onClick={this.onAddFilter.bind(this)}>
                <i><FontAwesomeIcon icon={faPlus} /></i>
                Add
              </div>
              <Popup ref={e => this.selectFilterPopup = e}>
                <div className={style.selectPopup}>
                  <h1>Filters</h1>
                  <div>
                  {
                    this.state.allFilters.length > 0
                    ? this.state.allFilters.map(f => <div key={f.name} onClick={() => this.onSelectFilter(f.name)}><h3>{f.name}</h3><p>{f.desc}</p></div>)
                    : (<span className={style.noFilters}>No filters found!</span>)
                  }
                  </div>
                </div>
              </Popup>
            </div>
          );
        }}
      </AppConsumer>
    );
  }
};