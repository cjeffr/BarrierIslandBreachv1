program breach_test

    implicit none
    save
    !  mu, sigma, lat0, lat1, lon0, lon1, 
    ! Place data here
    real(kind=8) :: sigma, start_time, end_time, time_ratio, breach_trigger, data
    real, allocatable :: num_breaches(:), mu(:), south(:), north(:), west(:), east(:)
    integer :: num
    ! Locals
    integer, parameter :: unit = 54
    character(len=128) :: line


    print *, "this does print"


        

            ! Open data file
            open(unit, file = 'breach.data')

	    read(unit, *) num
	    allocate (num_breaches(num), mu(num), south(num), north(num), west(num), east(num))
	    print *, num
            ! Basic switch to turn on variable friction
            read(unit, *)
            read(unit, *) num_breaches !breach_trigger
            read(unit, *) south
            read(unit, *) north
            read(unit, *) west
            read(unit, *) east
            read(unit, *) mu
            read(unit, *) sigma
            read(unit, *) time_ratio
            read(unit, *) start_time
            read(unit, *) end_time
            close(unit)
            print *, num_breaches, west, north




end program breach_test
