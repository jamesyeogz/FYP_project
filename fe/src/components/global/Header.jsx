import { Box, Typography } from '@mui/material'
import React from 'react'

const Header = ({Header,SubHeader}) => {
  return (
    <Box display="flex" flexDirection="row" alignItems="center" mb={2}>
    <Typography variant="h4" mr={4}>
      {Header}
    </Typography>
    <Typography variant="h2">{SubHeader}</Typography>
  </Box>
  )
}

export default Header