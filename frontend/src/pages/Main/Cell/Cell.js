import React, { useState } from 'react'
import styled from '@emotion/styled'
import cell_expanded from '../../../static/CellExpanded.png'

const CellHidden = styled.img`
  height: 88px;
  width: 100%;
  cursor: pointer;
`

const CellExpanded = styled.img`
  height: 700px;
  width: 100%;
`

export default function Cell(props) {
  const [expanded, setExpanded] = useState(true)

  const handleClick = () => {
    setExpanded(!expanded)
  }

  return (
      expanded ? 
      <CellHidden src={props.src} onClick={handleClick}/> : 
      <CellExpanded src={cell_expanded} onClick={handleClick}/>
  )
}