! try to  make something work with barrier breach
program barrier

implicit none
real :: slope, beach
real, allocatable, dimension(:) :: bathy
integer, dimension(5:5) :: test
integer :: i, j, mx, my , n, t1, t2, bathy_size
real :: xll, yll, cellsize, nodata_value, amp_max, dx, sigma, h0, x1, x2
real :: time(10) != (/(i, i=0,9, 1)/)
real, dimension(10) :: amp
real, dimension(1:10) :: time_test
integer, dimension(10) :: zero_array
integer, dimension(10) :: one_array
real(kind=8) :: values(10)
character(len=80) :: str
real :: x(11) = (/(i, i=-5,5, 1)/)
real, dimension(501) :: y = (/(i, i=-250, 250, 1)/)
real,allocatable, dimension(:,:) :: X_mesh, Y_mesh, breach

open(10, file='test.tt3')
	read(10,*) mx
	read(10,*) my
	read(10,*) xll
	read(10,*) yll
	read(10,*) cellsize
	read(10,*) nodata_value
close(10)
t1 = 3.0
t2 = 6.0
amp_max = 5.0
dx = 10.0/9.0 !((10) / (9))
time(1:10) = [(0 + ((i-1)*dx),i=1, 10)]

zero_array = 0
one_array = 1

do i = 1, 10
	if (time(i) < t1) then
		amp(i) = zero_array(i)
	elseif (t1 <= time(i) .and. time(i) < t2) then
		amp(i) =  (amp_max / (t2 - t1) * (time(i) - t1))
	elseif (t2 <= time(i)) then
		amp(i) = one_array(i) * amp_max
end if
	
end do


print *, 'This has run'
! print *,  SHAPE(bathy)
! allocate(bathy(1:mx*my))
! allocate(breach(1:bathy_size))
! open(11, file='test.tt3')
! do i=1,6
    ! read(11, *)
! end do
! print *, 'no error here'

! do j=1, my !*nrows
   ! read(11, *) (bathy((j-1)* mx + i),i=1,mx)
! end do
! print *, bathy(1:my*mx)
sigma = 10.0

X_mesh(:,:) = spread(x, 1, size(y))
Y_mesh(:,:) = spread(y, 2, size(x))
x1 = -25.0
x2 = 25.0
!print *, size(X_mesh,1), size(X_mesh, 2)
! do i=1, size(X_mesh, 1)
! print *, size(X_mesh(i,:))
print *, size(X_mesh(i,:)), size(X_mesh, 1)
allocate(breach(size(X_mesh, 1), size(X_mesh, 2)))
do i= 1, size(X_mesh,2)
	breach(:,i) = 10
	do j = 1, size(X_mesh,1)
		breach(j,:) = 10
end do
end do

do i = 1, size(amp)
	where (any(x1 <= X_mesh(:,:) .and. X_mesh(:,:) <= x2))
	!print *, amp(i)
		breach = breach - amp(i) * exp(-X_mesh**2 / sigma**2) * 0.10 * Y_mesh
	end where
end do

print *, breach
end program barrier
