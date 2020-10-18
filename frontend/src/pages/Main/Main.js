import React from 'react'
import styled from '@emotion/styled'
import search_bar from '../../static/SearchBar.png'
import cell_1 from '../../static/Cell_1.png'
import cell_2 from '../../static/Cell_2.png'
import cell_3 from '../../static/Cell_3.png'
import cell_4 from '../../static/Cell_4.png'
import cell_5 from '../../static/Cell_5.png'
import Cell from './Cell/Cell'

const Wrapper = styled.div`
`

const SearchBar = styled.img`
  height: 57px;
  width: 100%;
`

export default function Main() {
  return (
    <div>
      <SearchBar src={search_bar}/>
      <Cell src={cell_1}/>
      <Cell src={cell_2}/>
      <Cell src={cell_3}/>
      <Cell src={cell_4}/>
      <Cell src={cell_5}/>
    </div>
  )
}