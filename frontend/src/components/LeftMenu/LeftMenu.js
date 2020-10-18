import React from 'react'
import styled from '@emotion/styled'
import entity from '../../static/LeftMenu.png'

const Wrapper = styled.img`
  height: 100%;
  width: 18.28vw;
`

export default function LeftMenu() {
  return (
    <Wrapper src={entity}/>
  )
}