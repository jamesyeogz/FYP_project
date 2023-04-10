import { Box } from '@mui/material'
import React from 'react'
import Stock_Grid from '../../components/charts/Stock_Grid'

const Trades = () => {
  return (
    <Box p={2} height={"90vh"} width="100%" display={'flex'} justifyContent={'center'}>
      <Stock_Grid/>
    </Box>
  )
}

export default Trades