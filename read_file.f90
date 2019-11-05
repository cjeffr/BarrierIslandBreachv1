program read_file
    real(kind=8) :: mu, sigma, lat0, lat1, lon0, lon1, time, breach_trigger
    open(1, File='breach_test.txt', form='formatted')
    !    do i=1,7
    read(1, *) breach_trigger
    read(1, *) lat0
    read(1, *) lat1
    read(1, *) lon0
    read(1, *) lon1
    read(1, *) mu
    read(1, *) time
!        end do
    close(1)
    print *, breach_trigger, lat0, timecd
end program read_file